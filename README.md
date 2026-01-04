# piston-sim

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![GitHub release](https://img.shields.io/github/v/release/aa9772/piston-sim)

**piston-sim** is a Python project that simulates multiple pistons with endstop sensors, control commands, and fault handling. It uses **Matplotlib** for visualization, **Excel** for configuration, and **pyModbusTCP** for Modbus TCP communication. The simulation is modular and supports an arbitrary number of pistons, each with individual parameters.

---

## Features

- Multiple pistons with independent motion.
- Extend and retract commands via Modbus coils.
- Single-command pistons: retract automatically negates extend.
- Visualizes piston rods, heads, and cylinders.
- Endstop sensors with color coding (green = active, red = inactive).
- Fault simulation: pistons can be blocked via separate coils.
- Labels for each piston read from Excel.
- Smooth animation using Matplotlib `FuncAnimation`.
- Fully configurable via Excel.
- Sensors missing in Excel are automatically forced to 0.

---

## Requirements

- Python 3.8+
- Libraries:
  - `pandas`
  - `matplotlib`
  - `openpyxl`
  - `pyModbusTCP`

Install dependencies via pip:

```bash
pip install pandas matplotlib openpyxl pyModbusTCP

```

---


## Excel Configuration

The simulation reads piston parameters from an Excel file. Required columns:

| Column                  | Description                                         |
|-------------------------|-----------------------------------------------------|
| ID                      | Unique piston identifier                             |
| Label                   | Label displayed above the piston                     |
| Stroke                  | Maximum piston extension                             |
| Sensor Retract           | 'Yes'/'No', indicates presence of retract sensor   |
| Sensor Extend            | 'Yes'/'No', indicates presence of extend sensor    |
| Single/Double Command    | 'Single' or 'Double' command mode                  |
| Speed                   | Optional, speed of piston movement                 |

Example:

| ID | Label     | Stroke | Sensor Retract | Sensor Extend | Single/Double Command | Speed |
|----|----------|--------|----------------|---------------|---------------------|-------|
| 1  | Piston A | 0.4    | Yes            | Yes           | Double              | 0.05 |
| 2  | Piston B | 0.3    | Yes            | No            | Single              | 0.06 |

---

## How to Run

Run the main Python script with the Excel file path as argument:

```bash
python -m piston_sim.main path_to_your_excel.xlsx

```

If no argument is provided, the script uses pistons_config.xlsx in the project folder by default:

```bash
python -m piston_sim.main
```

---

## Modbus TCP Mapping

### Coils (R/W) – Commands
| Piston ID | Coil Offset | Function        |
|-----------|------------|----------------|
| i         | 2*i        | Extend command  |
| i         | 2*i + 1    | Retract command |

- Single-command pistons: the retract coil is ignored; retract = `not extend`.
- Double-command pistons: both extend and retract coils are used normally.

### Coils (R/W) – Fault / Block
| Piston ID | Coil Offset | Function       |
|-----------|------------|----------------|
| i         | 40 + i    | Fault / Block  |

### Discrete Inputs (R/O) – Sensors
| Piston ID | DI Offset  | Function           |
|-----------|------------|------------------|
| i         | 2*i        | Extended sensor   |
| i         | 2*i + 1    | Retracted sensor  |

- Sensors missing in Excel are automatically forced to 0.

---

## Code Structure

- `main.py` : main entry point, reads Excel, initializes pistons, PLCs, Modbus server, and animation.
- `piston.py` : defines the `Piston` class with stroke, sensors, label, motion logic, and fault handling.
- `plc.py` : simple PLC logic for command simulation.
- `visualization.py` : handles drawing pistons, rods, heads, sensors, command indicators, and labels.
- `shared_vars_modbus.py` : shared variables and Modbus TCP server (commands, faults, sensors).
- `config.py` : default simulation parameters (time step, simulation time, default speed).

---

## Visualization

- **Cylinder**: represents the piston body.
- **Rod**: moves along the cylinder, length equals piston stroke.
- **Piston Head**: at the end of the rod.
- **Endstop Sensors**: circles above the cylinder, green when active, red when inactive.
- **Command Indicators**: rectangles showing extend/retract command status.
- **Fault Indicators**: optional, highlight blocked pistons.
- **Labels**: displayed above each piston, read from Excel.

---

## Notes

- All pistons share the same X-axis scale for uniform visualization.
- Rod length is fixed per piston and matches the stroke.
- Sensor positions are aligned to be fully visible.
- Single-command pistons automatically negate retract from extend; double-command pistons use both coils.
- Fault coils block pistons without affecting commands.
- Warnings related to `color` and `edgecolor` in Matplotlib may appear but do not affect functionality.

---

## Future Improvements

- Support dynamic update of piston parameters during simulation.
- Export animation or simulation data to a file.
- Add more realistic physics (acceleration, deceleration, damping).
- Implement GUI for live configuration and fault toggling.

---

## Author

- Developed by Andrea, January 2026.
