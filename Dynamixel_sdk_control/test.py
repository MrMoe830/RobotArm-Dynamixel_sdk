from roboticstoolbox import *
import numpy as np
from control_dm import *

pi = np.pi
deg2rad = pi / 180

if __name__ == '__main__':
    lenof_link = 6
    dxl_id = [0, 1, 2, 3, 4, 5]
    length_arm = 0.081
    theta_start = [0] * lenof_link
    theta_goal = [0, 30, 0, -30, 0, 0]

    DHs = []
    for i in range(lenof_link - 1):
        DHs.append(RevoluteDH(a=length_arm, alpha=(pi / 2) * (-1) ** i))
    DHs.append(RevoluteDH(a=0.095, alpha=0, qlim=[-80 * pi / 180, 80 * pi / 180]))
    snake = DHRobot(DHs, name='arm')
    theta_goal = snake.toradians(theta_goal)
    # snake.teach(theta_goal, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    sol = jtraj(snake.q, theta_goal, 100)
    
    # When you execute the following motor control statement, if you find that the motor moves too fast, you can try to comment out the content of this line
    snake.plot(sol.q).hold()
    
    # ------- Dynamixel_X-motor control ------- #
    # motor = dxlControl_X('COM3')    # Incoming communication port number
    # motor.open_init_port(3000000)   # Set the port baud rate
    # motor.enable_torque(dxl_id)     # Pass in the motor ID, enable torque
    # motor.move2goal(motor.radarr2Pos(sol.q))    # Incoming motor position information, move to the target position
    # motor.disable_torque()    # disable torque
