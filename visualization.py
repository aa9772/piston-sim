import matplotlib.pyplot as plt

def draw_piston(ax, x: float, stroke: float, y_extended: bool, y_retracted: bool,
                u_extend: bool, u_retract: bool):
    """
    Draw a piston with sensors and command indicators.
    """
    ax.clear()
    rod_length = stroke
    # Adjust x-axis to fit rod + head
    ax.set_xlim(-0.2, stroke + rod_length + 0.1)
    ax.set_ylim(-0.3, 0.3)
    ax.axis("off")

    # Cylinder
    cylinder = plt.Rectangle((0, -0.05), stroke, 0.1, fill=True, facecolor='lightgrey', edgecolor='black')

    # Rod
    rod = plt.Rectangle((x, -0.015), rod_length, 0.03, facecolor='dimgray', edgecolor='black')

    # Head
    head = plt.Rectangle((x + rod_length, -0.03), 0.06, 0.06, facecolor='darkgrey', edgecolor='black')


    # Endstop sensors
    radius = 0.03
    ax.add_patch(plt.Circle((0, 0.15), radius, color='green' if y_retracted else 'red', ec='black', lw=1))
    ax.add_patch(plt.Circle((stroke, 0.15), radius, color='green' if y_extended else 'red', ec='black', lw=1))

    # Commands
    cmd_w = 0.08
    cmd_h = 0.04
    ax.add_patch(plt.Rectangle((0.1, 0.2), cmd_w, cmd_h, color='green' if u_extend else 'red', ec='black'))
    ax.text(0.1 + cmd_w/2, 0.2 + cmd_h/2, 'EXT', ha='center', va='center', fontsize=8, color='white')
    ax.add_patch(plt.Rectangle((0.2, 0.2), cmd_w, cmd_h, color='green' if u_retract else 'red', ec='black'))
    ax.text(0.2 + cmd_w/2, 0.2 + cmd_h/2, 'RET', ha='center', va='center', fontsize=8, color='white')

    # Exit if window closed
    if not plt.fignum_exists(ax.figure.number):
        plt.close('all')
        import sys
        sys.exit()
