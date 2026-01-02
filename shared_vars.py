"""
Shared variables for piston simulation.
Ready-to-communicate version.

This module contains variables that can be read or written by external systems,
such as PLC simulators, Excel, GUI dashboards, or network interfaces.

Each piston is indexed by its ID (integer).
"""

# ------------------------------
# Simulation parameters
# ------------------------------
SIM_TIME = 100.0      # Total simulation time [s] if using fixed DT
DT = 0.05             # Default simulation timestep [s]
DEFAULT_SPEED = 0.2   # Default piston speed [units/s]

# ------------------------------
# Faults
# ------------------------------
# Each piston can be blocked externally
# Example: piston_blocked[0] = True
piston_blocked = {}

# ------------------------------
# Commands (input from external system)
# ------------------------------
# Each piston can have extend/retract commands set externally
# Example: piston_commands[0] = {'extend': True, 'retract': False}
piston_commands = {}

# ------------------------------
# Sensors (output to external system)
# ------------------------------
# Each piston reports its sensor states
# Example: piston_sensors[0] = {'extended': False, 'retracted': True}
piston_sensors = {}

# ------------------------------
# Labels / identifiers
# ------------------------------
# Example: piston_labels[0] = 'Main Cylinder'
piston_labels = {}

# ------------------------------
# Maximum stroke for visualization
# ------------------------------
piston_max_stroke = 0.6

# ------------------------------
# Placeholder for external data
# ------------------------------
# Can be used for logs, monitoring, or any other system
external_data = {}
