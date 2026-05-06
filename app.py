import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

L1 = 187.0
L2 = 130.0
H1 = 195.5

def calculate_kinematics(theta1_deg, theta2_deg):
    t1 = np.radians(theta1_deg)
    t2 = np.radians(theta2_deg)
 
    x0, y0, z0 = 0, 0, 0
    
    x1, y1, z1 = 0, 0, H1
    
    x2 = L1 * np.cos(t1)
    y2 = L1 * np.sin(t1)
    z2 = H1
    
    x3 = x2 - L2 * np.cos(t2) * np.sin(t1)
    y3 = y2 + L2 * np.cos(t2) * np.cos(t1)
    z3 = z2 + L2 * np.sin(t2)
    
    return [x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.25)

limit = 400
ax.set_xlim([-limit, limit])
ax.set_ylim([-limit, limit])
ax.set_zlim([0, limit])
ax.set_xlabel('X Axis (mm)')
ax.set_ylabel('Y Axis (mm)')
ax.set_zlabel('Z Axis (mm)')
ax.set_title('3D Digital Twin - Custom 2-DOF Arm')

init_t1, init_t2 = 0.0, 0.0
xs, ys, zs = calculate_kinematics(init_t1, init_t2)

line, = ax.plot(xs, ys, zs, 'o-', color='#1f77b4', linewidth=5, markersize=8)
tcp_scatter, = ax.plot([xs[-1]], [ys[-1]], [zs[-1]], 'ro', markersize=10)

text_tcp = ax.text2D(0.05, 0.95, f"TCP Coordinate: X={xs[-1]:.1f}, Y={ys[-1]:.1f}, Z={zs[-1]:.1f}", 
                     transform=ax.transAxes, fontsize=12, color='red', weight='bold')

axcolor = 'lightgray'
ax_t1 = plt.axes([0.15, 0.12, 0.65, 0.03], facecolor=axcolor)
ax_t2 = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor=axcolor)

slider_t1 = Slider(ax_t1, 'Base Theta 1\n(0 to 300)', 0.0, 300.0, valinit=init_t1)
slider_t2 = Slider(ax_t2, 'Pitch Theta 2\n(-90 to 90)', -90.0, 90.0, valinit=init_t2)

def update(val):
    t1 = slider_t1.val
    t2 = slider_t2.val
    
    x, y, z = calculate_kinematics(t1, t2)
    
    line.set_data(x, y)
    line.set_3d_properties(z)
    
    tcp_scatter.set_data([x[-1]], [y[-1]])
    tcp_scatter.set_3d_properties([z[-1]])
    
    text_tcp.set_text(f"TCP Coordinate: X={x[-1]:.1f}, Y={y[-1]:.1f}, Z={z[-1]:.1f}")
    
    fig.canvas.draw_idle()

slider_t1.on_changed(update)
slider_t2.on_changed(update)

plt.show()