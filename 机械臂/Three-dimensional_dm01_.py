import math
import time
import numpy as np
from spatialmath import *
from roboticstoolbox import *
from spatialmath.base import *  # *********** - 矩阵相关库 - ***********l

from A_File_call import Function as ft

# ft.Cylinder()

pi = math.pi

if __name__ == '__main__':

    start_time = time.perf_counter()

    # --------------- Parameter settings --------------- #

    lenof_link = 8
    a_arm = 0.08
    RK = 6
    count = 0
    t = np.arange(0, 1, 0.01)
    theta_goal = [10, 10, -10, -10, 10, 10, -10, -10]
    theta_goal = ft.Degree_conversion(theta_goal)
    DHs = []

    # ------------------------------------------------------------------------------------------------------- #
    # Build Snake

    DHs.append(RevoluteDH(a=a_arm, alpha=(pi / 2), qlim=[-80 * pi / 180, 80 * pi / 180]))
    for i in range(1, lenof_link):
        DHs.append(RevoluteDH(a=a_arm, alpha=(pi / 2) * (-1) ** i, qlim=[-80 * pi / 180, 80 * pi / 180]))
    snake = DHRobot(DHs, name='arm')

    # print(snake.ets())
    # print(snake.ee_links)
    # snake.dhunique()
    # snake.dynamics_list()         # 打印动态DH参数表
    # snake.dynamics()  # 打印动态DH参数表
    snake2 = DHRobot(DHs[:-2])
    snake2.teach(theta_goal[:-2], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # end_time1 = time.perf_counter()

    # ------------------------------------------------------------------------------------------------------- #

    T0 = snake.fkine(snake.q)
    T_goal = snake.fkine_all(theta_goal)

    ####################################################################################################################
    # 入口对标用姿态矩阵

    T_rk = T_goal[RK - 1]
    T_rk_Next = T_goal[RK]
    T_rkA = T_rk.A.copy()
    T_rk_NextA = T_rk_Next.A.copy()
    T_rk_NextA[:, 3] = T_rkA[:, 3]

    T_RK = SE3(T_rk_NextA)  # 以九节姿态至八节位置的变换矩阵

    ####################################################################################################################
    # 执行器移至第八节

    Ts = ctraj(T0, T_RK, t)
    solq = [snake.q]
    for T in Ts:
        sol = snake.ikine_LMS(T, solq[-1])
        solq.append(sol.q)
    solq = np.array(solq)
    snake.plot(solq, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5]).hold()
    snake.teach(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # end_time2 = time.perf_counter()

    ####################################################################################################################
    # 入口校准，推进，末端校对

    for i in range(1, ((lenof_link - RK) // 2) + 1):
        solj = jtraj(solq[-1][-(i * 2):], theta_goal[-(lenof_link - RK): RK + i * 2], t)  # 末端角度值校准
        snake2 = DHRobot(DHs[:-(i * 2)])
        snake2.q = solq[-1][:-(i * 2)]
        T0 = snake2.fkine(snake2.q)
        Ts = ctraj(T0, T_RK, t)
        solq1 = []
        for T in Ts:
            sol = snake2.ikine_LMS(T, solq[-1][: -(i * 2)])
            solq1.append(sol.q)
        solq1 = np.array(solq1)
        solq = np.r_[solq, np.c_[solq1, solj.q]]

        del snake2
    # end_time3 = time.perf_counter()

    # for i in range(len(solq)):
    #     for j in range(len(solq[-1])):
    #         if solq[i][j] > pi / 2 or solq[i][j] < (-pi / 2):
    #             print(solq[i])
    #             count = count + 1
    #             break
    # # print(count)
    # print(solq)

    # end_time_all = time.perf_counter()
    # print('Snake创建用时:', end_time1 - start_time)
    # print('Snake移至第八节用时:', end_time2 - end_time1)
    # print('Snake解算轨迹用时:', end_time3 - end_time2)
    # print('Snake运动总时长:', end_time_all - start_time)

    snake.plot(solq, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5]).hold()
    snake.teach(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    snake.teach(theta_goal, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
