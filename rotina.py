import rtde_control
import rtde_io
import threading
import rtde_receive
import time


# rtde_r = rtde_receive.RTDEReceiveInterface(HOST)
rtde_io = rtde_io.RTDEIOInterface("10.224.1.90")
rtde_c = rtde_control.RTDEControlInterface("10.224.1.90")

def main():
    rtde_io.setStandardDigitalOut(0, True)
    print("main")

def rotina1():
    rtde_io.setStandardDigitalOut(1, True)
    print("rotina1")

def rotina2():
    rtde_io.setStandardDigitalOut(2, True)
    print("rotina2")

th_main = threading.Thread(target=main)
th_rotina1 = threading.Thread(target=rotina1)
th_rotina2 = threading.Thread(target=rotina2)

th_rotina2.start()
th_main.start()
th_rotina1.start()