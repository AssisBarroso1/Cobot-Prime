import rtde_receive
import rtde_io
import rtde_control
import time
import threading


HOST = "10.224.1.90" # ip adress

rtde_c = rtde_control.RTDEControlInterface(HOST)

inicio =  time.time()
while True:
    
    rtde_c.teachMode()
    
    fim = time.time()
    
    print(fim - inicio)

    if (fim - inicio) > 60:
        
        rtde_c.endTeachMode()
        
        break