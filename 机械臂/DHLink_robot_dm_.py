import numpy as np
from spatialmath import *
from roboticstoolbox import *
from spatialmath.base import *

pi = np.pi

if __name__ == '__main__':
    lenof_link = 12
    a_arm = 0.08
    RK_pos = 8
    t = np.arange(0, 1, 0.01)
    count = 0

    JOINT_LIMIT = [-80 * pi / 180, 80 * pi / 180]
    LINK_QUALITY = 0.6
    ACC_GRAVITY = [0, 0, -9.81]

    JOINT_LIMIT_BASE = [-70 * pi / 180, 70 * pi / 180]

    DHLs = [DHLink(alpha=pi / 2, a=a_arm, qlim=JOINT_LIMIT_BASE, m=LINK_QUALITY)]
    for i in range(1, lenof_link):
        DHLs.append(DHLink(alpha=(pi / 2) * (-1) ** i, a=0.08, qlim=JOINT_LIMIT, m=LINK_QUALITY))
    snake = DHRobot(name='arm', links=DHLs, gravity=ACC_GRAVITY)
    # print(snake.gravload(snake.q))

    theta_end = [25.5, 36.3, 19.2, 6.0, -25.8, -32.4, -40.4, -22.0, -12.5, 32.0, 34.4, 26.0]
    theta_end = snake.toradians(theta_end)

    T0 = snake.fkine(snake.q)
    T_end = snake.fkine_path(theta_end)
    X_rot = SE3(trotx(-90, 'deg', [0, 0, 0]))

    T_rk = T_end[RK_pos]

    Ts = ctraj(T0, T_rk, t)
    solq = [snake.q]
    for T in Ts:
        sol = snake.ikine_min(T, solq[-1], True, method='L-BFGS-B')
        solq.append(sol.q)
    solq = np.array(solq)

    snake.plot(solq, limits=[0, 1.0, -0.5, 0.5, -0.5, 0.5]).hold()
