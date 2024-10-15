import rtde_receive
import rtde_io
import rtde_control
import time
import threading
HOST = "10.224.1.90"

rtde_c = rtde_control.RTDEControlInterface(HOST)
rtde_r = rtde_receive.RTDEReceiveInterface(HOST)
rtde_io_ = rtde_io.RTDEIOInterface(HOST)

# global botao
global y
global input1
global botao

botao = 0
input1 = 0
y = 0 #quantidade de peças que foram transportadas
x = 4 #quantidade de peças a serem transportadas
# botao = 0


posicaoA = [0.2828900504494836, -0.24975101068866634, 0.35255218635007146, 0.39447710968522615, 3.116727805079671, 2.6646095827690376e-11] #posição de referência 
posicaoB = [0.1293005895433933, -0.7292112842885596, -0.09036771194919306, 0.34933088597410444, 3.1221102371858036, -3.86606358180079e-11] #Uma posição acima antes de pegar a primeira peça
posicaoC = [0.12719657070539037, -0.7294648773631294, -0.1543760625905667, 0.3451673476885476, 3.122567720860938, -8.690216002901498e-05]#posição pegando a primeira peça
posicaoD = [0.7357640956424341, -0.1175988945511068, 0.02318929263842176, 0.34654277044078863, 3.1224209372339566, 1.0237594390970328e-11]#Uma posição acima antes de deixar a primeira peça
posicaoE = [0.7371173459544346, -0.11875484235206787, -0.15591167988555143, 0.34845381469968933, 3.1222082473604034, 9.948140293098993e-12]#posição soltando a primeira peça


def botaoPressionado():
    global botao
    global input1
    while True:
        input1 = rtde_r.getDigitalInState(1)
        print(botao)
        if input1:
            botao += 1
            
            if botao % 2 != 0:
                rtde_c.disconnect()
                time.sleep(1)
            else:
                rtde_c.reconnect()
                time.sleep(1)

def pegar():
    #fecha a ferramenta e pega a peça
    rtde_io_.setToolDigitalOut(1, True) # Reseta 1
    rtde_io_.setToolDigitalOut(0, False)  # Seta 0
    time.sleep(0.5)


def soltar():
    
    global y
    
    # robô abre a ferramenta
    rtde_io_.setToolDigitalOut(1, False) # Reseta 1
    rtde_io_.setToolDigitalOut(0, True)  # Seta 0
    y = y + 1
    print(y)
    time.sleep(0.5)
    
def posicionarFerramentaParaPegar():
    
    #robô move a ferramenta para a posição de origem
    rtde_c.moveL(posicaoA,speed=0.2,acceleration=0.3) 
    time.sleep(0.5)
    
    # robô abre a ferramenta
    rtde_io_.setToolDigitalOut(1, False) # Reseta 1
    rtde_io_.setToolDigitalOut(0, True)  # Seta 0
    
    if y != 0 :
        #robô move a ferramenta para a posição B
        rtde_c.moveL(posicaoB,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
        
        #ajustar a ferramenta para pegar a peça
        posicaoC[0] = posicaoC[0] - 0.027
        posicaoC[1] = posicaoC[1] + 0.027
        rtde_c.moveL(posicaoC,speed=0.2,acceleration=0.3)
        time.sleep(0.1)
        pegar()
        #ajustar a ferramenta para erguer a peça
        posicaoB[0] = posicaoB[0] - 0.027
        posicaoB[1] = posicaoB[1] + 0.027
        rtde_c.moveL(posicaoB,speed=0.2,acceleration=0.3)
        
        #robô move a ferramenta para a posição de origem
        rtde_c.moveL(posicaoA,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
        
    else:
        #robô move a ferramenta para a posição B
        rtde_c.moveL(posicaoB,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
        
         # Posiciona a ferramente sobre a peça 
        rtde_c.moveL(posicaoC,speed=0.2,acceleration=0.3)
        time.sleep(0.5)
            
        pegar()
                
        #Eleva a peça para a posição B
        rtde_c.moveL(posicaoB,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
            
        #robô move a ferramenta para a posição de origem
        rtde_c.moveL(posicaoA,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
            
        

def posicionarFerramentaParaSoltar():
    #Uma posição acima antes de deixar a primeira peça
    rtde_c.moveL(posicaoD,speed=0.2,acceleration=0.3) 
    time.sleep(0.5)
    
    if y != 0:
        #ajustar a ferramenta para largar a peça
        posicaoE[2] = posicaoE[2] + 0.029
        rtde_c.moveL(posicaoE,speed=0.2,acceleration=0.3)
        
        time.sleep(0.5)
        
        soltar()
        
        #elevar a peça para a posição D
        rtde_c.moveL(posicaoD,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
        
        #robô move a ferramenta para a posição de origem
        rtde_c.moveL(posicaoA,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
    
    else: 
        #ajustar a ferramenta para largar a peça
        # a peça está pronta para ser solta
        rtde_c.moveL(posicaoE,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)
            
        #peça solta
        soltar()
            
        #elevar a peça para a posição D
        rtde_c.moveL(posicaoD,speed=0.2,acceleration=0.3) 
        time.sleep(0.5)

def contadorDePecas():
        while True:
            global y
            # print("meu y", y)
            if y == 2:
                #print("foram duas peças")
                rtde_io_.setStandardDigitalOut(0,True)
                time.sleep(1)
            if y == 4:
                
                rtde_io_.setStandardDigitalOut(0,True)
                rtde_io_.setStandardDigitalOut(1,True)
                time.sleep(1)
                #print("foram 4 peças")
    
#começo do código
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