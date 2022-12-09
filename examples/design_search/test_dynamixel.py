'''
code for testing dynamixel XL430 W250T motors
'''

import os
import time
import timeit

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

sleeptest       = 0.02
index           = 0
positionStep    = 81   
PWM             = 100

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
BAUDRATE                    = 3000000

TorqueLimit                 = 10       # Torque Limit 0-855 for XL 430 W250

# Factory default ID of all DYNAMIXEL is 1
DXL_ID                      = 1

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = 'COM7'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(2.0)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# PWM MODE 
#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, 11, 16) # PWM MODE


# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
#dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, 36, TorqueLimit) # Torque Limit 
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

while 1:
    print("Press any key to continue! (or press ESC to quit!)",)
    if getch() == chr(0x1b):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, 65, 0) # LED OFF
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, 65, 0) # LED OFF
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        break
        
    # dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, 1000)    
    
    if index == 0:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, 65, 1 ) # LED ON
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, 65, 1 ) # LED ON
        for i in range(DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE, positionStep):

            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, i)
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 2, ADDR_GOAL_POSITION, i)
            #print(i)
            #t = timeit.timeit
            #print(t)
            time.sleep(sleeptest)
            
            #if i == DXL_MAXIMUM_POSITION_VALUE:
            #    break
        index = 1
    
    else:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, 65, 0) # LED OFF
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, 65, 0) # LED OFF        
        for i in reversed(range(DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE, positionStep)):

            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, i)
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, 2, ADDR_GOAL_POSITION, i)
            #print(i)
            #t = timeit.timeit
            #print(t)
            time.sleep(sleeptest)
            
            #if i == DXL_MAXIMUM_POSITION_VALUE:
            #    break
            index = 0         
    
