import numpy
from dynamixel_sdk import *


# noinspection PyAttributeOutsideInit,PyShadowingBuiltins,GrazieInspection
class dxlControl_X(object):
    """
    Provides group operation support and control for X-series motors in Dynamixel products,
    which can be used for multi-motor cooperative operation.(为Dynamixel产品中的X系电机提供组操作支持和控制，可用于多电机协同作业)
    You can use with robotics-toolbox

    .. Note::
    Before formally executing the motor control program, please be sure to check the following points to prevent
    the program from failing:
            - When the program is running, please ensure that you are in an absolutely safe area.

            - Please do not forget to turn on the power supply and ensure that the power supply
              module of the unit can work normally.

            - Please check whether all motors in the unit are powered properly.

            - Make sure the communication port is available and connected

    """

    def __init__(self, port_name: str):
        """
        Control Table Address

        :param port_name: port_name: the port name of the Dynamixel
        :type port_name: str

        .. note::
        port naming convention:
                - Windows: "COM*", \n
                - Linux: "/dev/ttyUSB*", \n
                - Mac: "/dev/tty.usbserial-*"

        """
        assert isinstance(port_name, str)
        self.ADDR_TORQUE_ENABLE = 64
        self.ADDR_GOAL_POSITION = 116
        self.ADDR_PRESENT_POSITION = 132
        self.LEN_GOAL_POSITION = 4  # Data Byte Length
        self.LEN_PRESENT_POSITION = 4  # Data Byte Length
        self.DXL_MINIMUM_POSITION_VALUE = 0  # Refer to the Minimum Position Limit of product eManual
        self.DXL_MAXIMUM_POSITION_VALUE = 4095  # Refer to the Maximum Position Limit of product eManual
        self.BAUDRATE = 57600
        self.PROTOCOL_VERSION = 2.0
        self.DEVICENAME = port_name  # Ubuntu/Windows串口
        self.TORQUE_ENABLE = 1  # Value for enabling the torque
        self.TORQUE_DISABLE = 0  # Value for disabling the torque
        self.DXL_MOVING_STATUS_THRESHOLD = 3  # Dynamixel moving status threshold

    def __init(self):
        """
        Initialize the port and the communication protocol version
        """
        # Initialize PortHandler instance # Set the port path
        self.portHandler = PortHandler(self.DEVICENAME)
        # Init PacketHandler instance and Set the protocol version
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)
        # Initialize GroupSyncWrite instance
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, self.ADDR_GOAL_POSITION,
                                             self.LEN_GOAL_POSITION)
        # Initialize GroupSyncRead instace for Present Position
        self.groupSyncRead = GroupSyncRead(self.portHandler, self.packetHandler, self.ADDR_PRESENT_POSITION,
                                           self.LEN_PRESENT_POSITION)

    def open_init_port(self, baud_rate: int):
        """
        Open and initialize the communication port

        :param baud_rate: baud rate of the communication port
        :type baud_rate: int

        """
        self.__init()
        assert isinstance(baud_rate, int)
        self.BAUDRATE = baud_rate
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port!", "Press any key to terminate...", sep='\n')
            sys.exit()
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate", "Press any key to terminate...", sep='\n')
            sys.exit()

    def enable_torque(self, IDs: list):
        """
        Turn on Dynamixl-Xmotor torque

        :param IDs: A list of the ID names of all motors in the group
        :type IDs: list[int]

        Example:
            ``IDs=[0,1,2,3,4,5,6,7,8]``

        .. Note:: IDs should start from zero，and should be continuous

        """
        assert isinstance(IDs, list)
        self.IDs = IDs
        for id in self.IDs:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id,
                                                                           self.ADDR_TORQUE_ENABLE,
                                                                           self.TORQUE_ENABLE)

            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel#%d has been successfully connected" % id)

    def move2goal(self, goalPoss):
        """
        :param goalPoss: the Position of every motor
        :type goalPoss: numpy.ndarray

        """
        # goalPos = goalPos / (np.pi * 2) * 4096 + 2048
        self.enable_torque(self.IDs)
        assert isinstance(goalPoss, numpy.ndarray)

        # 为 Dynamixel 当前位置值添加参数存储
        for id in self.IDs:
            print(id)
            dxl_addparam_result = self.groupSyncRead.addParam(id)
            if not dxl_addparam_result:
                print("[ID:%03d] groupSyncRead add param failed" % id)
                sys.exit()
        for goalPos in goalPoss:
            self.dxl_goal_position = goalPos
            # 将目标位置值分配到字节数组中
            for id in self.IDs:
                param_goal_position = [DXL_LOBYTE(DXL_LOWORD(int(self.dxl_goal_position[id]))),
                                       DXL_HIBYTE(DXL_LOWORD(int(self.dxl_goal_position[id]))),
                                       DXL_LOBYTE(DXL_HIWORD(int(self.dxl_goal_position[id]))),
                                       DXL_HIBYTE(DXL_HIWORD(int(self.dxl_goal_position[id])))]
                # 将Dynamixel[id]目标位置添加到Sync-write参数存储
                dxl_addparam_result = self.groupSyncWrite.addParam(id, param_goal_position)
                if not dxl_addparam_result:
                    print("[ID:%03d] groupSyncWrite add param failed" % id)
                    sys.exit()
            # Sync-write goal position
            dxl_comm_result = self.groupSyncWrite.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            # Clear sync-write parameter storage
            self.groupSyncWrite.clearParam()
            while True:
                # Sync-read present position
                dxl_comm_result = self.groupSyncRead.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                for id in self.IDs:
                    # Check if groupsyncread data of Dynamixel is available
                    dxl_getdata_result = self.groupSyncRead.isAvailable(id, self.ADDR_PRESENT_POSITION,
                                                                        self.LEN_PRESENT_POSITION)
                    if not dxl_getdata_result:
                        print("[ID:%03d] groupSyncRead getdata failed" % id)
                        sys.exit()
                # 获取 Dynamixel 当前位置值
                for id in self.IDs:
                    dxl_present_position = self.groupSyncRead.getData(id, self.ADDR_PRESENT_POSITION,
                                                                      self.LEN_PRESENT_POSITION)
                    print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t" % (id, self.dxl_goal_position[id], dxl_present_position))
                finish = False
                for id in self.IDs:
                    dxl_present_position = self.groupSyncRead.getData(id, self.ADDR_PRESENT_POSITION,
                                                                      self.LEN_PRESENT_POSITION)
                    if not (abs(self.dxl_goal_position[id] - dxl_present_position) > self.DXL_MOVING_STATUS_THRESHOLD):
                        finish = True
                        break
                if finish:
                    break
        # Clear sync-read parameter storage
        self.groupSyncRead.clearParam()

    def disable_torque(self):
        """
        Turn off the torque of Dynamixl-Xmotor,and close the communication port
        """
        for id in self.IDs:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id,
                                                                           self.ADDR_TORQUE_ENABLE,
                                                                           self.TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # Close port
        self.portHandler.closePort()

    @staticmethod
    def radarr2Pos(goalPos):
        """
        Convert the data in the array to motor-identifiable data (motor position)

        Note
        ------
        If your data comes from robots-toolbox, you should call this function interface first to realize data conversion

        """
        assert isinstance(goalPos, numpy.ndarray)
        return goalPos / (numpy.pi * 2) * 4096 + 2048


if __name__ == '__main__':
    d = dxlControl_X('/dev/ttyUSB0')
    d.open_init_port(3000000)
    d.enable_torque([0, 1, 2, 3, 4, 5])
    d.move2goal(numpy.array([2048, 2048, 2048, 2048, 2048, 2048]))
    d.disable_torque()
