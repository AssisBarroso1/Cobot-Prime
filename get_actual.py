import rtde_receive

rtde_r = rtde_receive.RTDEReceiveInterface("10.224.1.90")

actual_q = rtde_r.getActualQ()

actual_tcp = rtde_r.getTargetTCPPose()

actual_tcp_target = rtde_r.getActualTCPPose()

print("Actual_q:", actual_q)
print("Actual_q:", actual_tcp)
print("Actual_q:", actual_tcp_target)