import math
import numpy as np
from roboticstoolbox import *

pi = math.pi
du = pi / 180  # 度
radian = 180 / pi  # 弧度

if __name__ == '__main__':
    lenof_link = 10  # 轴
    detT = 0.1  # 采样时间步长
    DHs = []
    S = [0, 90, 0, -90, 0, -90, 0, 90, 0, 0]  # 角度

    # 目标末位置角度转弧度
    sta = [0] * lenof_link
    end = []
    for i in range(lenof_link):
        end.append(S[i] / 180 * pi)
    S0 = end  # 保存初始机械臂姿态

    Speed = np.matrix([[0], [0], [0], [0], [0], [0]])  # 末端运动速度

    ###  Orthogonal structure
    for i in range(lenof_link):
        j = -1
        DHs.append(RevoluteDH(a=2, alpha=(pi / 2) * j ** i))
    snake = DHRobot(DHs, name="Arm")

    Ssave = np.zeros([100, lenof_link])
    for i in range(100):
        Jsave = snake.jacob0(S)
        iJ = np.linalg.pinv(Jsave)
        detq = np.dot(np.asarray(iJ), np.asarray(Speed))
        end = end + detq.T * detT
        Ssave[i] = end
    sol1 = jtraj(sta, end, 100)
    W = snake.fkine(end)
    print(W)
    snake.plot(sol1.q, limits=[0, 20, -0.5, 0.5, -10, 10]).hold()
