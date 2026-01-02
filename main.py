import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from config import DT, SIM_TIME, DEFAULT_SPEED
from piston import Piston
from plc import SimplePLC
from shared_vars import piston_commands, piston_sensors, piston_blocked

def main(file_path):
    # Read configuration from Excel
    df = pd.read_excel(file_path)

    pistons = []
    plcs = []
    for idx, row in df.iterrows():
        stroke = row['Stroke']
        piston = Piston(stroke=stroke, speed=row.get('Speed', DEFAULT_SPEED))
        piston.has_retract_sensor = row.get('Sensor Retract', 'Yes') == 'Yes'
        piston.has_extend_sensor = row.get('Sensor Extend', 'Yes') == 'Yes'
        piston.single_command = row.get('Single/Double Command', 'Double') == 'Single'
        label = row.get('Label', f'Piston {idx+1}')  # default label if missing
        piston.label = label
        plc = SimplePLC()
        pistons.append(piston)
        plcs.append(plc)

    for idx, piston in enumerate(pistons):
        # Initialize dictionaries for external communication
        piston_commands[idx] = {'extend': False, 'retract': False}
        piston_blocked[idx] = False
        piston_sensors[idx] = {'extended': False, 'retracted': False}


    n = len(pistons)
    fig, axes = plt.subplots(n, 1, figsize=(6, 2*n))
    if n == 1:
        axes = [axes]

    # Find maximum stroke for uniform axis scaling
    max_stroke = max(p.stroke for p in pistons)

    patches_list = []
    for piston, ax in zip(pistons, axes):
        # Set fixed axes to prevent scaling issues
        ax.set_xlim(0, max_stroke + piston.stroke + 0.1)
        ax.set_ylim(-0.3, 0.3)
        ax.axis('off')

        # Draw cylinder representing piston body
        cylinder = plt.Rectangle((0, -0.05), piston.stroke, 0.1, fill=True, color='lightgrey', edgecolor='black')
        ax.add_patch(cylinder)

        # Draw rod with length = piston stroke (fixed length for this piston)
        rod_length = piston.stroke
        rod = plt.Rectangle((piston.x, -0.015), rod_length, 0.03, color='dimgray', edgecolor='black')
        ax.add_patch(rod)

        # Draw piston head
        head = plt.Rectangle((piston.x + rod_length, -0.03), 0.06, 0.06, color='darkgrey', edgecolor='black')
        ax.add_patch(head)

        # Draw sensors
        sensor_retract = plt.Circle((0.05, 0.15), 0.03, color='red', ec='black', lw=1)
        sensor_extend = plt.Circle((piston.stroke, 0.15), 0.03, color='red', ec='black', lw=1)
        ax.add_patch(sensor_retract)
        ax.add_patch(sensor_extend)

        # Draw command indicators
        cmd_extend = plt.Rectangle((0.1, 0.2), 0.08, 0.04, color='red', ec='black')
        cmd_retract = plt.Rectangle((0.2, 0.2), 0.08, 0.04, color='red', ec='black')
        ax.add_patch(cmd_extend)
        ax.add_patch(cmd_retract)

        # Add label above piston
        label_text = ax.text(0, 0.3, piston.label, ha='center', va='center', fontsize=10, fontweight='bold')

        # Store references to patches for animation update
        patches_list.append({
            'rod': rod,
            'head': head,
            'sensor_retract': sensor_retract,
            'sensor_extend': sensor_extend,
            'cmd_extend': cmd_extend,
            'cmd_retract': cmd_retract,
            'rod_length': rod_length,
            'label_text': label_text
        })

    def update(frame):
        for i, (piston, plc, ax_patches) in enumerate(zip(pistons, plcs, patches_list)):

            # ======== READ EXTERNAL COMMANDS =========
            cmd = piston_commands.get(i, {})
            piston.u_extend = cmd.get('extend', False)
            piston.u_retract = cmd.get('retract', False)

            # ======== APPLY BLOCK FAULT ============
            piston.blocked = piston_blocked.get(i, False)

            # ======== STEP PLC AND PISTON ==========
            plc.step(piston.y_extended, piston.y_retracted)
            piston.step(piston.u_extend, piston.u_retract, DT)

            # ======== UPDATE SENSOR STATES ==========
            piston_sensors[i] = {
                'extended': piston.y_extended,
                'retracted': piston.y_retracted
            }

            # ======== UPDATE VISUALIZATION ==========
            ax_patches['rod'].set_x(piston.x)
            ax_patches['head'].set_x(piston.x + ax_patches['rod_length'])
            if piston.has_retract_sensor:
                ax_patches['sensor_retract'].set_color('green' if piston.y_retracted else 'red')
            else:
                ax_patches['sensor_retract'].set_color('grey')
            if piston.has_extend_sensor:
                ax_patches['sensor_extend'].set_color('green' if piston.y_extended else 'red')
            else:
                ax_patches['sensor_extend'].set_color('grey')
            ax_patches['cmd_extend'].set_color('green' if piston.u_extend else 'red')
            ax_patches['cmd_retract'].set_color('green' if piston.u_retract else 'red')

    # Create animation
    anim = FuncAnimation(fig, update, frames=int(SIM_TIME/DT), interval=DT*1000)
    plt.show()

if __name__ == "__main__":
    import os
    # Use default Excel file if no argument is provided
    if len(sys.argv) < 2:
        default_file = os.path.join(os.path.dirname(__file__), "pistons_config.xlsx")
        print(f"No Excel file provided, using default: {default_file}")
        excel_path = default_file
    else:
        excel_path = sys.argv[1]

    main(excel_path)