# shared_vars_modbus.py
"""
Shared variables and Modbus TCP server for piston simulation.
- Commands (extend/retract) as contiguous Coils
- Fault / Block as separate Coils
- Sensors as Discrete Inputs
- Supports multiple pistons
"""

from pyModbusTCP.server import ModbusServer

# --- Global variables ---
piston_commands = {}  # {piston_index: {'extend': bool, 'retract': bool}}
piston_faults = {}    # {piston_index: bool}  # coil for forcing block
piston_sensors = {}   # {piston_index: {'extended': 0/1, 'retracted': 0/1}}
pistons_flags = {}    # {piston_index: {'has_extend_sensor': True/False, 'has_retract_sensor': True/False}}
piston_labels = {}    # {piston_index: label}

server = None

# --- Initialize variables ---
def init_pistons(n_pistons):
    """
    Initialize piston variables and start Modbus server.
    """
    global piston_commands, piston_faults, piston_sensors, pistons_flags, piston_labels, server
    for i in range(n_pistons):
        piston_commands[i] = {'extend': False, 'retract': False}
        piston_faults[i] = False
        piston_sensors[i] = {'extended': 0, 'retracted': 0}
        pistons_flags[i] = {'has_extend_sensor': True, 'has_retract_sensor': True}
        piston_labels[i] = f"Piston {i+1}"

    # Start Modbus server if not already running
    if server is None:
        server = ModbusServer(host="0.0.0.0", port=5020, no_block=True)
        server.start()  # <-- Correct way to start pyModbusTCP server


# --- Update commands from Modbus Coils ---
def update_commands_from_modbus():
    """
    Read piston extend/retract commands from Coils.
    - 2*i -> extend
    - 2*i+1 -> retract
    """
    for i in piston_commands:
        try:
            vals = server.data_bank.get_coils(2*i, 2)
            piston_commands[i]['extend'] = bool(vals[0])
            piston_commands[i]['retract'] = bool(vals[1])
        except Exception:
            piston_commands[i]['extend'] = False
            piston_commands[i]['retract'] = False


# --- Update faults from Modbus Coils ---
def update_faults_from_modbus():
    """
    Read piston fault/block from separate coils.
    - i -> fault/block, starting offset 100
    """
    for i in piston_faults:
        try:
            val = server.data_bank.get_coils(len(piston_commands) * 2 + i, 1)  # starting offset from last command coils
        except Exception:
            piston_faults[i] = False


# --- Write sensors to Modbus Discrete Inputs ---
def write_sensors_to_modbus():
    """
    Write piston sensors to Discrete Inputs.
    - 2*i -> extended sensor
    - 2*i+1 -> retracted sensor
    Sensors missing are forced to 0.
    """
    for i in piston_sensors:
        flags = pistons_flags.get(i, {'has_extend_sensor': True, 'has_retract_sensor': True})
        ext = int(piston_sensors[i].get('extended', 0) if flags.get('has_extend_sensor', True) else 0)
        ret = int(piston_sensors[i].get('retracted', 0) if flags.get('has_retract_sensor', True) else 0)
        server.data_bank.set_discrete_inputs(2*i, [ext])
        server.data_bank.set_discrete_inputs(2*i+1, [ret])
