# piston-sim

This Python project simulates multiple pistons with endstop sensors and control commands using **Matplotlib** for visualization and **Excel** for configuration. The simulation is modular and supports an arbitrary number of pistons, each with individual parameters.

---

## Features

- Simulates multiple pistons with independent motion.
- Supports **extend** and **retract** commands.
- Visualizes **rod**, **piston head**, and **cylinder**.
- Shows **endstop sensors** with color indication (green = active, red = inactive).
- Supports **labels for each piston** read from Excel.
- Animation is handled using **Matplotlib `FuncAnimation`**.
- Fully configurable via **Excel file**.

---

## Requirements

- Python 3.8+
- Libraries:
  - pandas
  - matplotlib
  - openpyxl (for reading Excel files)

Install requirements via pip:

```bash
pip install pandas matplotlib openpyxl
```

---

## Excel Configuration

The simulation reads piston parameters from an Excel file. Required columns:

| Column                     | Description                                |
|-----------------------------|--------------------------------------------|
| ID                          | Piston identifier                          |
| Label                       | Label to display above the piston          |
| Stroke                      | Maximum extension of the piston            |
| Sensor Retract               | 'Yes' or 'No', indicates presence of retract sensor |
| Sensor Extend                | 'Yes' or 'No', indicates presence of extend sensor  |
| Single/Double Command        | 'Single' or 'Double' command mode          |
| Speed                       | Optional, speed of piston movement         |

Example:

| ID | Label     | Stroke | Sensor Retract | Sensor Extend | Single/Double Command | Speed |
|----|----------|--------|----------------|---------------|---------------------|-------|
| 1  | Piston A | 0.4    | Yes            | Yes           | Double              | 0.05 |
| 2  | Piston B | 0.3    | Yes            | No            | Single              | 0.06 |

---

## How to Run

Run the main Python script with the Excel file path as argument:

```bash
python main.py path_to_excel.xlsx
```

If no argument is provided, the script uses `pistons_config.xlsx` in the project folder by default.

```bash
python main.py
```

---

## Code Structure

- `main.py` : main entry point, reads Excel, initializes pistons, PLCs, and animation.
- `piston.py` : defines the `Piston` class with stroke, sensors, label, and motion logic.
- `plc.py` : simple PLC logic for command simulation.
- `visualization.py` : handles drawing pistons, rods, heads, sensors, and labels.
- `config.py` : default simulation parameters (time step, simulation time, default speed).

---

## Visualization

- **Cylinder**: represents the piston body.
- **Rod**: moves along the cylinder, length equals piston stroke.
- **Piston Head**: at the end of the rod.
- **Endstop Sensors**: circles above the cylinder, green when active, red when inactive.
- **Command Indicators**: rectangles showing extend/retract command status.
- **Labels**: displayed above each piston, read from Excel.

---

## Notes

- The simulation ensures all pistons share the same X-axis scale for uniform visualization.
- The rod length is fixed per piston and matches the stroke, not changing during movement.
- Sensor positions are aligned to be fully visible and correctly indicate endstop status.
- Warnings related to `color` and `edgecolor` in Matplotlib may appear but do not affect functionality.

---

## Future Improvements

- Support dynamic update of piston parameters during simulation.
- Add user interface for live configuration.
- Export animation or simulation data to a file.
- Add more realistic physics (acceleration, deceleration, damping).

---

## Author

- Developed by Andrea, January 2026.

