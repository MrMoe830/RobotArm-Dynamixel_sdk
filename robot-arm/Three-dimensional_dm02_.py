import time
import numpy as np
from roboticstoolbox import *
from dynamixel_sdk import *
from spatialmath import *

from A_File_call import *

pi = np.pi

if __name__ == '__main__':

    lenof_link = 8
    a_arm = 0.08
    RK = 6
    count = 0
    t = np.arange(0, 1, 0.01)
    t1 = np.arange(0.1, 1.1, 0.1)
    theta_end = [0, 36, 29, 23, 20, -30, -26, -51]
    DHs = [RevoluteDH(a=a_arm, alpha=pi / 2, qlim=[-70 * pi / 180, 70 * pi / 180])]
    for i in range(1, lenof_link):
        DHs.append(RevoluteDH(a=a_arm, alpha=(pi / 2) * (-1) ** i, qlim=[-75 * pi / 180, 75 * pi / 180]))
    snake = DHRobot(DHs, name="arm")
    theta_end = snake.toradians(theta_end)
    # snake.teach(theta_end, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])

    T0 = snake.fkine(snake.q)
    T_goal = snake.fkine_all(theta_end)
    # print(T_goal)

    T_rk = T_goal[RK].copy()
    # T_rk_Next = T_goal[7]
    # T_rkA = T_rk.A.copy()
    # T_rk_NextA = T_rk_Next.A.copy()
    # T_rk_NextA[:, 3] = T_rkA[:, 3]

    Ts = ctraj(T0, T_rk, t)
    solq = [snake.q]
    for T in Ts:
        sol = snake.ikine_min(T, solq[-1], qlim=True, method='L-BFGS-B')
        solq.append(sol.q)
    solq = np.array(solq)
    # T_rk_theta = snake.fkine_all(solq[-1])
    # snake2 = DHRobot(DHs[:-2])
    # snake2.teach(solq[-1][:-2], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # snake.plot(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # snake.teach(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])

    for i in range(1, ((lenof_link - RK) // 2) + 1):
        solj = jtraj(solq[-1][-(i * 2):], theta_end[-(lenof_link - RK): RK + i * 2], t)  # 末端角度值校准
        snake2 = DHRobot(DHs[:-(i * 2)])
        snake2.q = solq[-1][:-(i * 2)]
        T0 = snake2.fkine(snake2.q)
        Ts = ctraj(T0, T_rk, t)
        solq1 = []
        for T in Ts:
            sol = snake2.ikine_min(T, solq[-1][: -(i * 2)], qlim=True, method='L-BFGS-B')
            solq1.append(sol.q)
        solq1 = np.array(solq1)
        solq = np.r_[solq, np.c_[solq1, solj.q]]
        del snake2
    # snake.teach(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # snake.teach(theta_end, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])

    # 角度筛查
    for i in range(len(solq)):
        for j in range(len(solq[-1])):
            if solq[i][j] > 90 * pi / 180 or solq[i][j] < -90 * pi / 180:
                print(solq[i])
                count = count + 1
                break
    print('>90° or <-90°关节配置:\t', count)

    snake.plot(solq, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    snake.teach(solq[-1], limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])
    # snake.teach(theta_end, limits=[0, 0.7, -0.5, 0.5, -0.5, 0.5])

    # q_motor = Pos_conversion(solq)
    # ready(lenof_link)
    # for i in range(len(q_motor)):
    #     work(q_motor[i])
    #     # time.sleep(0.02)
    # time.sleep(20)
    # gg(lenof_link)

    # T_ = snake.fkine_all(solq[-1])
    # T1_ = T_
    # T1A_ = T1_.A
    # T1A_copy = T1A_.copy()
    # _T_ = T1A_copy[6:]
    # xyz1_end = _T_[0][:3, 3]
    # xyz2_end = _T_[1][:3, 3]
    # xyz3_end = _T_[2][:3, 3]
    #
    # xyz_1 = []
    # xyz_2 = []
    # xyz_3 = []
    # for i in range(101, solq.shape[0]):
    #     T_t = snake.fkine_all(solq[i])
    #     T_t1 = T_t
    #     T_t1A = T_t1.A
    #     T_t_copy = T_t1A.copy()
    #     _T_ = T_t_copy[6:]
    #     xyz1 = _T_[0][:3, 3]  # 倒数第三个连杆末端xyz
    #     xyz_1.append(xyz1)
    #     xyz2 = _T_[1][:3, 3]  # 倒数第二个连杆末端xyz
    #     xyz_2.append(xyz2)
    #     xyz3 = _T_[2][:3, 3]  # 最后一个连杆末端xyz
    #     xyz_3.append(xyz3)
    # xyz_1 = np.array(xyz_1)  # 100组q值对应的倒数第三个连杆末端xyz值，100*3
    # xyz_2 = np.array(xyz_2)  # 100组q值对应的倒数第二个连杆末端xyz值，100*3
    # xyz_3 = np.array(xyz_3)  # 100组q值对应的最后一个连杆末端xyz值，100*3
    # xyz = np.c_[xyz_1, xyz_2, xyz_3]
    #
    # xyz_distance = []
    # for i in range(100):
    #     x1_dis = xyz_1[i][0] - xyz1_end[0]
    #     y1_dis = xyz_1[i][1] - xyz1_end[1]
    #     z1_dis = xyz_1[i][2] - xyz1_end[2]
    #     x2_dis = xyz_2[i][0] - xyz2_end[0]
    #     y2_dis = xyz_2[i][1] - xyz2_end[1]
    #     z2_dis = xyz_2[i][2] - xyz2_end[2]
    #     x3_dis = xyz_3[i][0] - xyz3_end[0]
    #     y3_dis = xyz_3[i][1] - xyz3_end[1]
    #     z3_dis = xyz_3[i][2] - xyz3_end[1]
    #     xyz1_dis = math.sqrt(x1_dis ** 2 + y1_dis ** 2 + z1_dis ** 2)
    #     xyz2_dis = math.sqrt(x2_dis ** 2 + y2_dis ** 2 + z2_dis ** 2)
    #     xyz3_dis = math.sqrt(x3_dis ** 2 + y3_dis ** 2 + z3_dis ** 2)
    #     xyz_distance.append(xyz1_dis)
    #     xyz_distance.append(xyz2_dis)
    #     xyz_distance.append(xyz3_dis)
    # xyz_distance_max = max(xyz_distance)
    # print('最大偏移量:\t', xyz_distance_max)

    # T_goal1 = T_goal
    # T_goal1A = T_goal1.A
    # T_goal_copy = T_goal1A.copy()
    # T_ = T_goal_copy[6:]
    # xyz1_end = T_[0][:3, 3]  # 目标构型下倒数第三个连杆末端xyz值
    # xyz2_end = T_[1][:3, 3]  # 目标构型下倒数第二个连杆末端xyz值
    # xyz3_end = T_[2][:3, 3]  # 目标构型下最后一个连杆末端xyz值
    # xyz_end_xl1 = [xyz2_end[0] - xyz1_end[0], xyz2_end[1] - xyz1_end[1], xyz2_end[2] - xyz1_end[2]]  # 末态倒数第二节连杆向量
    # xyz_end_xl2 = [xyz3_end[0] - xyz2_end[0], xyz3_end[1] - xyz2_end[1], xyz3_end[2] - xyz2_end[2]]  # 末态最后一节连杆向量
    # print(T_)     # True

    # xyz1Sam_point_end = []
    # xyz2Sam_point_end = []
    # for time_Step in t1:
    #     x1Sam_point_end = xyz1_end[0] + xyz_end_xl1[0] * time_Step  # 倒数第二个连杆采样点的x值
    #     y1Sam_point_end = xyz1_end[1] + xyz_end_xl1[1] * time_Step  # 倒数第二个连杆采样点的y值
    #     z1Sam_point_end = xyz1_end[2] + xyz_end_xl1[2] * time_Step  # 倒数第二个连杆采样点的z值
    #     x2Sam_point_end = xyz2_end[0] + xyz_end_xl2[0] * time_Step  # 最后一个连杆采样点的x值
    #     y2Sam_point_end = xyz2_end[1] + xyz_end_xl2[1] * time_Step  # 最后一个连杆采样点的y值
    #     z2Sam_point_end = xyz2_end[2] + xyz_end_xl2[2] * time_Step  # 最后一个连杆采样点的z值
    #     xyz1Sam_point_end.append([x1Sam_point_end, y1Sam_point_end, z1Sam_point_end])  # 倒数第二个连杆采样点xyz值
    #     xyz2Sam_point_end.append([x2Sam_point_end, y2Sam_point_end, z2Sam_point_end])  # 最后一个连杆采样点xyz值
    # xyz1Sam_point_end = np.array(xyz1Sam_point_end)  # 倒数第二个连杆点采样数据，10*3
    # xyz2Sam_point_end = np.array(xyz2Sam_point_end)  # 最后一个连杆点采样数据，10*3
    # print(xyz1Sam_point_end[-1], xyz2Sam_point_end[-1])  # True
    # xyz_1 = []
    # xyz_2 = []
    # xyz_3 = []
    # # print(solq.shape)
    # for i in range(101, solq.shape[0]):
    #     T_t = snake.fkine_all(solq[i])  # True
    #     T_t1 = T_t
    #     T_t1A = T_t1.A
    #     T_t_copy = T_t1A.copy()
    #     _T_ = T_t_copy[6:]
    #     __T = SE3(T_t_copy)
    #     # 后三个矩阵坐标对应的xyz坐标值
    #     xyz1 = _T_[0][:3, 3]  # 倒数第三个连杆末端xyz
    #     xyz_1.append(xyz1)
    #     xyz2 = _T_[1][:3, 3]  # 倒数第二个连杆末端xyz
    #     xyz_2.append(xyz2)
    #     xyz3 = _T_[2][:3, 3]  # 最后一个连杆末端xyz
    #     xyz_3.append(xyz3)
    # xyz_1 = np.array(xyz_1)  # 100组q值对应的倒数第三个连杆末端xyz值，100*3
    # xyz_2 = np.array(xyz_2)  # 100组q值对应的倒数第二个连杆末端xyz值，100*3
    # xyz_3 = np.array(xyz_3)  # 100组q值对应的最后一个连杆末端xyz值，100*3
    # xyz = np.c_[xyz_1, xyz_2, xyz_3]  # 后两个电机对应的三个连杆末端的xyz坐标值(真实值)，100*9
    # # print(xyz_2[-1], xyz_3[-1])
    # xyz1_xl = []
    # xyz2_xl = []
    # x1_xl = []
    # y1_xl = []
    # z1_xl = []
    # x2_xl = []
    # y2_xl = []
    # z2_xl = []
    # for xyzE in xyz:
    #     x1xl = xyzE[3] - xyzE[0]
    #     y1xl = xyzE[4] - xyzE[1]
    #     z1xl = xyzE[5] - xyzE[2]
    #     x2xl = xyzE[6] - xyzE[3]
    #     y2xl = xyzE[7] - xyzE[4]
    #     z2xl = xyzE[8] - xyzE[5]
    #     x1_xl.append(x1xl)
    #     y1_xl.append(y1xl)
    #     z1_xl.append(z1xl)
    #     x2_xl.append(x2xl)
    #     y2_xl.append(y2xl)
    #     z2_xl.append(z2xl)
    #     xyz1_xl.append([x1xl, y1xl, z1xl])  # 倒数第二个线段向量值
    #     xyz2_xl.append([x2xl, y2xl, z2xl])  # 最后一个线段向量值
    # x1_xl = np.array(x1_xl)  # 倒数第二个连杆的x向量值,100*1
    # y1_xl = np.array(y1_xl)  # 倒数第二个连杆的y向量值,100*1
    # z1_xl = np.array(z1_xl)  # 倒数第二个连杆的z向量值,100*1
    # x2_xl = np.array(x2_xl)  # 最后一个连杆的x向量值
    # y2_xl = np.array(y2_xl)  # 最后一个连杆的y向量值
    # z2_xl = np.array(z2_xl)  # 最后一个连杆的z向量值
    # xyz1_xl = np.array(xyz1_xl)  # 倒数第二个连杆对应向量,100*3
    # xyz2_xl = np.array(xyz2_xl)  # 最后一个连杆对应向量,100*3
    # # print(x1_xl.shape, xyz2_xl.shape)
    # # 对末端两连杆进行点采样，每组q值每个连杆取10个样点
    # xyz1Sam_point = []
    # xyz2Sam_point = []
    # for i in range(xyz.shape[0]):
    #     for time_Step in t1:
    #         x1Sam_point = xyz_1[i][0] + x1_xl[i] * time_Step
    #         y1Sam_point = xyz_1[i][1] + y1_xl[i] * time_Step
    #         z1Sam_point = xyz_1[i][2] + z1_xl[i] * time_Step
    #         x2Sam_point = xyz_2[i][0] + x2_xl[i] * time_Step
    #         y2Sam_point = xyz_2[i][1] + y2_xl[i] * time_Step
    #         z2Sam_point = xyz_2[i][2] + z2_xl[i] * time_Step
    #         xyz1Sam_point.append([x1Sam_point, y1Sam_point, z1Sam_point])
    #         xyz2Sam_point.append([x2Sam_point, y2Sam_point, z2Sam_point])
    # xyz1Sam_point = np.array(xyz1Sam_point)  # 1000*3，每十行为一组q生成的倒数第二节连杆的样点xyz值，共一百组
    # xyz2Sam_point = np.array(xyz2Sam_point)  # 1000*3，每十行为一组q生成的最后一节连杆的样点xyz值，共一百组
    # xyzSam_point = np.c_[xyz1Sam_point, xyz2Sam_point]  # 最后两节连杆的采样点xyz值，1000*6,10个一组
    # # print(xyz1Sam_point[-1], xyz2Sam_point[-1])
    #
    # xyz_distance = []
    # xyz1_dis = []
    # xyz2_dis = []
    # for xyz in xyzSam_point:
    #     for i in range(10):
    #         x1_dis = xyzSam_point[-(10 - i)][0] - xyz[0]
    #         y1_dis = xyzSam_point[-(10 - i)][1] - xyz[1]
    #         z1_dis = xyzSam_point[-(10 - i)][2] - xyz[2]
    #         x2_dis = xyzSam_point[-(10 - i)][3] - xyz[3]
    #         y2_dis = xyzSam_point[-(10 - i)][4] - xyz[4]
    #         z2_dis = xyzSam_point[-(10 - i)][5] - xyz[5]
    #         xyz1_dis.append(math.sqrt(x1_dis ** 2 + y1_dis ** 2 + z1_dis ** 2))
    #         xyz2_dis.append(math.sqrt(x2_dis ** 2 + y2_dis ** 2 + z2_dis ** 2))
    #     xyz1_dis_min = min(xyz1_dis)
    #     xyz2_dis_min = min(xyz1_dis)
    #     xyz_distance.append(xyz1_dis_min)
    #     xyz_distance.append(xyz2_dis_min)
    # xyz_distance_max = max(xyz_distance)
    # xyz_distance = np.array(xyz_distance)
    # print(xyz_distance_max)
