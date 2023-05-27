import pygame
from pygame import mixer
import random
import math
import time

#Iniciar pygame
pygame.init()

#Craer la pantalla
pantalla = pygame.display.set_mode((800,600))
pygame.key.set_repeat(1,25) 

#Titulo, icono y Fondo
pygame.display.set_caption("Viaje a la tierra")
icono = pygame.image.load("ovnicat.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("spacex.png")

#Añadir musica de fondo
mixer.music.load('Browser_History.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#Texto final
texto = pygame.font.Font('pixel.ttf',92)

def texto_final(x,y):
    texto1 = "Te quedaste sin vida"
    texto = fuente.render(f"{texto1}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


################################################################################################################
#Jugador
class Jugador():

    #Coordenadas iniciales
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.imagen = pygame.image.load("cat-orange.png")
        self.balas_disponibles = []
    
    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))
    
    #Solo mover, qui se tiene en cuenta la presion continua de la tecla ademas se llama al limite para que este no pase
    def mover(self,presion):
        self.presion = presion 
        if self.presion[pygame.K_LEFT]:
            self.x -= 5
        if self.presion[pygame.K_RIGHT]:
            self.x += 5
        if self.presion[pygame.K_UP]:
            self.y -= 5
        if self.presion[pygame.K_DOWN]:
            self.y += 5
        self.limite()

    #Disparar balas que a su vez llama a la clase balas y las añade a las balas disponibles para que cada una sea unica
    def disparar(self):
        self.bala = Bala(self.x,self.y)
        self.balas_disponibles.append(self.bala)

    #Definir limites para evitar que el personaje salga de la pantalla
    def limite(self):
        if self.x <= 0:
            self.x = 0
        if self.x >= 300:
            self.x = 300
        if self.y <= 0:
            self.y = 0
        if self.y >= 500:
            self.y = 500

#Clase para la bala del personaje 
class Bala():

    #Se inicia con las coordenadas que le de el personaje principal y que se sumen unos cuantos pixeles para que quede centrado
    def __init__(self,x,y):
        self.x = x + 20
        self.y = y + 36
        self.imagen = pygame.image.load("bala.png")
        self.disparos_img = pygame.image.load("bala.png")
        self.disparos_x_mov = 1

    #Si se dibuja la bala por ende debe existir un movimiento
    def dibujar(self):
        pantalla.blit(self.disparos_img , (self.x ,self.y))
        self.disparo_movimiento()

    #La funcion que define el movimiento
    def disparo_movimiento(self):
        self.x += self.disparos_x_mov

#Se crea al personaje principal con una coordenada inicial
personaje = Jugador(0, 210)

class Vida():

    def __init__(self,x,y):
        self.imagen = pygame.image.load("vida.png")
        self.x = x
        self.y = y

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

#Se crean las vidas del personaje
vida = []
puntaje = 0
contador = 500
fuente = pygame.font.Font('pixel.ttf',32)

def puntaje_total(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

for v in range(3):
    vida.append(Vida(contador,10))
    contador += 100

###########################################################################################################

#Enemigo de tipo_1 Los que se mueven de arriba a abajo
class Enemigo_tipo1():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemigo_img = pygame.image.load("enemy-cat.png")
        self.mov_y = 1
        self.mov_x = 30
        self.cartucho = []
        self.disparos_x_mov = 1

    def dibujar(self):
        pantalla.blit(self.enemigo_img, (self.x, self.y))
    
    def mover(self):
        self.y += self.mov_y
        if self.y >= 500:
            self.mov_y = -1
            self.x -= self.mov_x
        if self.y <= 0:
            self.mov_y = 1
            self.x -= self.mov_x
    
    def disparar(self):
        self.bala = Bala_enemigo(self.x,self.y)
        self.cartucho.append(self.bala)

#Clase para la bala del enemigo
class Bala_enemigo():

    #Se inicia con las coordenadas que le de el enemigo y que se sumen unos cuantos pixeles para que quede centrado
    def __init__(self,x,y):
        self.x = x + 20
        self.y = y + 36
        self.imagen = pygame.image.load("bala.png")
        self.disparos_img = pygame.image.load("bala-enemigo.png")
        self.disparos_x_mov = 3

    #Si se dibuja la bala por ende debe existir un movimiento
    def dibujar(self):
        pantalla.blit(self.disparos_img , (self.x ,self.y))
        self.disparo_movimiento()

    #La funcion que define el movimiento
    def disparo_movimiento(self):
        self.x -= self.disparos_x_mov
    
#Enemigo de tipo_2 Los que se mueven en una sola direccion. 
class Enemigo_tipo2():
    enemigo_img = pygame.image.load("asteroid.png")
    mov_y , mov_x = 1, 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dibujar(self):
        pantalla.blit(self.enemigo_img, (self.x, self.y))
    
    def mover(self):
        self.x -= self.mov_x
################################################################################################################################
#Generar el tipo de enemigo aleatorio

enemigos = []
def generar_enemigo():
    tipo_enemigo = [Enemigo_tipo1, Enemigo_tipo2]
    for enemigo in range(10):
        enemigo_random = random.choice(tipo_enemigo)
        x = random.randint(650, 900)
        y = random.randint(0, 500)
        yield enemigos.append(enemigo_random(x, y))

def eliminar(enemigo):
    enemigos.remove(enemigo)


############################################################################################################################

#Para carlcular la distancia del enemigo

def distancia(x1,y1,x2,y2):
    pit_distancia = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
    if pit_distancia < 80:
        return True
    else:
        return False


inicio = True
presionado = False

while inicio:
    pantalla.blit(fondo, (0,0))

    for evento in pygame.event.get():
        
        if evento.type == pygame.QUIT:
            inicio = False

        #Evento que verifica si fue presionado la barra espaciadora y dispara segun el toque
        if evento.type == pygame.KEYDOWN:
            if not presionado and evento.key == pygame.K_SPACE:
                disparo = mixer.Sound('pop.mp3')
                disparo.play()
                personaje.disparar()
                presionado = True
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                presionado = False
        
                
                
        #Movimiento del personaje principal
        presion = pygame.key.get_pressed()
        if presion:
            personaje.mover(presion)



    #Ciclo que sirve para mostrar todos los enemigos 
    for enemigo in enemigos:
        enemigo.dibujar()
        enemigo.mover()
        numero = random.randint(1, 30)
        choque= distancia(personaje.x, personaje.y, enemigo.x, enemigo.y)

        #Si el enemigo pertenece a la clase tipo 1, dispara

        if isinstance(enemigo, Enemigo_tipo1):
            #Si el numero random que se genero anteriormente esta en el rango entre 5 y 15 que dispare
            if numero >= 5 and numero <= 15:
                enemigo.disparar()

                #Solo dispara 2 y se van eliminando si pasa fuera de la pantalla
                for laser in enemigo.cartucho:
                    if len(enemigo.cartucho) <= 2:
                        laser.dibujar()
                        disparo_enemigo = distancia(personaje.x, personaje.y, laser.x - 30, laser.y - 30)
                        if laser.x <= -30:
                            enemigo.cartucho.remove(laser)
                        if disparo_enemigo:
                            enemigo.cartucho.remove(laser)
                            vida.pop(0)
                    else:
                        enemigo.cartucho.pop()

        if enemigo.x < -100:
            eliminar(enemigo)

        if choque:
            eliminar(enemigo)
            muerte = mixer.Sound('bomb.mp3')
            muerte.play()
            vida.pop(0)


    #MCiclo para mostrar las balas que fueron disparadas hasta 10 balas.
    for bala in personaje.balas_disponibles:

        if len(personaje.balas_disponibles) <= 5:
            bala.dibujar()
            if bala.x >= 800:
                personaje.balas_disponibles.remove(bala)
        else:
            personaje.balas_disponibles.pop()

        #Si una bala toca al enemigo
        for enemigo in enemigos:
            choque= distancia(bala.x, bala.y, enemigo.x, enemigo.y)
            if choque:
                muerte = mixer.Sound('bomb.mp3')
                muerte.play()
                eliminar(enemigo)
                personaje.balas_disponibles.remove(bala)
                puntaje += 1

    #Mostrar la vida del personaje 

    if len(vida) > 0:
        #Generar solo 5 enemigos
        personaje.dibujar()
        if len(enemigos) < 5 :
            next(generar_enemigo())
        for v in vida:
            v.dibujar()
    else:
        #Si la vida es menos de 0 entonces termino el juego :D
        enemigos.clear()
        texto_final(250,250)

    #Mostrar al dibujo
    

    puntaje_total(10,10)
    
    pygame.display.update()
