import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# พารามิเตอร์ของโครงสร้างแขนกล (หน่วย mm)
# ==========================================
L1, L2, H1 = 187.0, 130.0, 195.5

def calculate_kinematics(theta1_deg, theta2_deg):
    t1, t2 = np.radians(theta1_deg), np.radians(theta2_deg)
    x0, y0, z0 = 0, 0, 0
    x1, y1, z1 = 0, 0, H1
    x2, y2, z2 = L1 * np.cos(t1), L1 * np.sin(t1), H1
    
    x3 = x2 - L2 * np.cos(t2) * np.sin(t1)
    y3 = y2 + L2 * np.cos(t2) * np.cos(t1)
    z3 = z2 + L2 * np.sin(t2)
    
    return [x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3]

# ==========================================
# ส่วนแสดงผลบนหน้าเว็บ
# ==========================================
st.set_page_config(page_title="2-DOF Arm Digital Twin")
st.title("Robotic Arm 3D Kinematics")

# สร้าง Slider บนเว็บ
t1 = st.slider("Base Theta 1 (0 to 300 องศา)", 0.0, 300.0, 0.0)
t2 = st.slider("Pitch Theta 2 (-90 to 90 องศา)", -90.0, 90.0, 0.0)

# คำนวณพิกัด
x, y, z = calculate_kinematics(t1, t2)

# แสดงตัวเลขพิกัด
st.success(f"**TCP Coordinate:** X = {x[-1]:.1f}, Y = {y[-1]:.1f}, Z = {z[-1]:.1f}")

# วาดกราฟ 3 มิติ
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
limit = 400
ax.set_xlim([-limit, limit])
ax.set_ylim([-limit, limit])
ax.set_zlim([0, limit])
ax.set_xlabel('X Axis (mm)')
ax.set_ylabel('Y Axis (mm)')
ax.set_zlabel('Z Axis (mm)')

# พล็อตเส้นและจุด
ax.plot(x, y, z, 'o-', color='#1f77b4', linewidth=5, markersize=8)
ax.plot([x[-1]], [y[-1]], [z[-1]], 'ro', markersize=10)

# ส่งกราฟไปแสดงบน Streamlit
st.pyplot(fig)