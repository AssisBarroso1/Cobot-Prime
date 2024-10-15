import rtde_control as c
import rtde_io as io
import time
import rtde_receive as r

HOST = "10.224.1.90"

rtde_io_ = io.RTDEIOInterface(HOST)
rtde_c = c.RTDEControlInterface(HOST)
rtde_r = r.RTDEReceiveInterface(HOST)

rtde_io_.setToolDigitalOut(1, False) # Reseta 1
rtde_io_.setToolDigitalOut(0, True)  # Seta 0

## Posição da base ##
base = [2.180025339126587, -1.1723782581141968, 1.9706876913653772, -2.368596216241354, -1.5668438116656702, -5.195293132458822]

## Posições onde a peça deve ser pega ##
p1 = [0.12719657070539037, -0.7294648773631294, -0.1543760625905667, 0.3451673476885476, 3.122567720860938, -8.690216002901498e-05]
p2 = [0.7371173459544346, -0.11875484235206787, -0.15591167988555143, 0.34845381469968933, 3.1222082473604034, 9.948140293098993e-12]

inc = 0.05
num_pecas = 4

## Posições onde a peça deve ser deixada ##

try:
    for i in range(num_pecas):
        # Calcular a nova posição de coleta
        p1 = p1.copy()
        p1[0] += i * inc  # Incremento na posição x
        p1[1] += i * inc  # Incremento na posição y
        
        # Mover para a posição de coleta
        c.moveL(base, 0.2, 0.1)
        c.moveL(p1, 0.2, 0.1)
        time.sleep(1)
        rtde_io_.setToolDigitalOut(1, True)
        time.sleep(1)
        c.moveL(base)
        # print(f"Movido para posição de coleta {i+1}: {p1}")

        # Calcular a nova posição de entrega
        p2 = p2.copy()
        p2[2] += i * inc  # Incremento na posição z
        
        # Mover para a posição de entrega
        c.moveL(p2, 0.2, 0.1)
        # print(f"Movido para posição de entrega {i+1}: {p2}")
        
        # Simular entrega da peça (pode incluir comando para controle do gripper)
        time.sleep(1)  # Tempo para entrega da peça
        
    # print("Todas as peças foram movidas com sucesso!")

finally:
    # Desconectar do robô
    rtde_c.disconnect()
    rtde_r.disconnect()







# try:
#     while True:
#         rtde_c.moveJ(p1, 0.2, 0.5)
#         # time.sleep(1)

#         rtde_c.moveJ(move_A, 0.2, 0.5)
#         # time.sleep(1)

#         rtde_c.moveJ(move_B, 0.2, 0.5)
#         # time.sleep(1)

# except KeyboardInterrupt:
#     print("Stop")

# finally:
#     rtde_c.stopScript()



