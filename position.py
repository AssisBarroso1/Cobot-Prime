import rtde_receive
import rtde_io
import rtde_control
import time

HOST = "10.224.1.90"

# rtde_r = rtde_receive.RTDEReceiveInterface(HOST)

rtde_io = rtde_io.RTDEIOInterface(HOST)
rtde_c = rtde_control.RTDEControlInterface(HOST)

# rtde_io.setToolDigitalOut(1, True)
# rtde_io.setToolDigitalOut(0, False)

#actual_q = rtde_r.getActualQ()
# actual_tcp = rtde_r.getTargetTCPPose()

#print("Posição TCP Atual = ", actual_tcp)
# print("Posição Articulação Atual = ", actual_q)

move_A = [0.5286191940964514, -0.37493501829029374, 0.3146101626494903, 0.8858762408410674, 2.971753189123485, 0.446721289554079]

move_B = [0.5286191940964514, -0.37493501829029374, 0.3146101626494903, 0.8858762408410674, 2.971753189123485, 0.446721289554079]


for i in range(3):
    rtde_c.moveL(move_A, 0.3, 0.3)
    time.sleep(0.1)
    rtde_c.moveL(move_B, 0.3, 0.3)
