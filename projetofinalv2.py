import rtde_receive
import rtde_io
import rtde_control
import time
import threading

HOST = "10.224.1.90"

rtde_c = rtde_control.RTDEControlInterface(HOST)
rtde_r = rtde_receive.RTDEReceiveInterface(HOST)
rtde_io_ = rtde_io.RTDEIOInterface(HOST)

botao_lock = threading.Lock()
botao = 0
input1 = 0
y = 0  # quantidade de peças que foram transportadas
x = 4  # quantidade de peças a serem transportadas

posicaoA = [0.2828900504494836, -0.24975101068866634, 0.35255218635007146, 0.39447710968522615, 3.116727805079671, 2.6646095827690376e-11]
posicaoB = [0.1293005895433933, -0.7292112842885596, -0.09036771194919306, 0.34933088597410444, 3.1221102371858036, -3.86606358180079e-11]
posicaoC = [0.12719657070539037, -0.7294648773631294, -0.1543760625905667, 0.3451673476885476, 3.122567720860938, -8.690216002901498e-05]
posicaoD = [0.7357640956424341, -0.1175988945511068, 0.02318929263842176, 0.34654277044078863, 3.1224209372339566, 1.0237594390970328e-11]
posicaoE = [0.7371173459544346, -0.11875484235206787, -0.15591167988555143, 0.34845381469968933, 3.1222082473604034, 9.948140293098993e-12]

def botaoPressionado():
    global botao
    global input1
    while True:
        input1 = rtde_r.getDigitalInState(1)
        with botao_lock:
            if input1:
                botao += 1
                if botao % 2 != 0:
                    rtde_c.disconnect()
                else:
                    rtde_c.reconnect()
        time.sleep(1)

def pegar():
    rtde_io_.setToolDigitalOut(1, True)  # Reseta 1
    rtde_io_.setToolDigitalOut(0, False)  # Seta 0
    time.sleep(0.5)

def soltar():
    global y
    rtde_io_.setToolDigitalOut(1, False)  # Reseta 1
    rtde_io_.setToolDigitalOut(0, True)  # Seta 0
    y += 1
    print(y)
    time.sleep(0.5)

def posicionarFerramentaParaPegar():
    global y
    rtde_c.moveL(posicaoA, speed=0.2, acceleration=0.3)
    time.sleep(0.5)

    rtde_io_.setToolDigitalOut(1, False)  # Reseta 1
    rtde_io_.setToolDigitalOut(0, True)  # Seta 0

    posB = posicaoB.copy()
    posC = posicaoC.copy()

    if y != 0:
        posC[0] -= 0.027
        posC[1] += 0.027
        rtde_c.moveL(posC, speed=0.2, acceleration=0.3)
        time.sleep(0.1)
        pegar()
        posB[0] -= 0.027
        posB[1] += 0.027
        rtde_c.moveL(posB, speed=0.2, acceleration=0.3)
        rtde_c.moveL(posicaoA, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
    else:
        rtde_c.moveL(posicaoB, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        rtde_c.moveL(posicaoC, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        pegar()
        rtde_c.moveL(posicaoB, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        rtde_c.moveL(posicaoA, speed=0.2, acceleration=0.3)
        time.sleep(0.5)

def posicionarFerramentaParaSoltar():
    global y
    rtde_c.moveL(posicaoD, speed=0.2, acceleration=0.3)
    time.sleep(0.5)

    posE = posicaoE.copy()

    if y != 0:
        posE[2] += 0.029
        rtde_c.moveL(posE, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        soltar()
        rtde_c.moveL(posicaoD, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        rtde_c.moveL(posicaoA, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
    else:
        rtde_c.moveL(posicaoE, speed=0.2, acceleration=0.3)
        time.sleep(0.5)
        soltar()
        rtde_c.moveL(posicaoD, speed=0.2, acceleration=0.3)
        time.sleep(0.5)

def contadorDePecas():
    global y
    while True:
        if y == 2:
            rtde_io_.setStandardDigitalOut(0, True)
        if y == 4:
            rtde_io_.setStandardDigitalOut(0, True)
            rtde_io_.setStandardDigitalOut(1, True)
        time.sleep(1)

def main():
    for i in range(x):
        posicionarFerramentaParaPegar()
        posicionarFerramentaParaSoltar()

Th_main = threading.Thread(target=main)
Th_rotina1 = threading.Thread(target=contadorDePecas)
Th_rotina2 = threading.Thread(target=botaoPressionado)

Th_main.start()
Th_rotina1.start()
Th_rotina2.start()

Th_main.join()
Th_rotina1.join()
Th_rotina2.join()