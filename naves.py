import pygame
import random

FPS = 30
ANCHO = 1000
ALTO = 800
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)

HC74225 = (199,66,37)
H61CD35 = (97,205,53)
H8E89A6 = (142, 137, 166)



class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #rectangulo jugador
        # self.image = pygame.Surface((200,200))
        # self.image.fill(VERDE)
        self.image = pygame.image.load("elementos/nave-espacial.png")
        self.image.set_colorkey(H8E89A6)
        self.rect = self.image.get_rect()
        self.rect.center = (400 , 600)

        #velocidad inicial (quieto)
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        #movimiento lineal a la izquierda
        # self.rect.x -= 10
        # if self.rect.right < 0:
        #     self.rect.left = ANCHO

        #velocidad predeterminada
        self.velocidad_x = 0
        self.velocidad_y = 0
        
        #mantiene las techas pulsadas
        teclas = pygame.key.get_pressed()
        #mueve a la izquierda
        if teclas[pygame.K_a]:
            self.velocidad_x = -10

        #mueve a la derecha
        if teclas[pygame.K_d]:
            self.velocidad_x = 10
        
        #mueve arriba
        if teclas[pygame.K_w]:
            self.velocidad_y = -10
        
        #mueve abajo
        if teclas[pygame.K_s]:
            self.velocidad_y = 10

        #dispara
        if teclas[pygame.K_SPACE]:
            jugador.disparo()
        
        #actualiza la posicion del personaje
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        #limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0

        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

        #limita el margen arriba
        if self.rect.top < 400:
            self.rect.top = 400

        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

    def disparo(self):
        disparo = Disparo(self.rect.centerx, self.rect.top + 5)
        balas.add(disparo)


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #rectangulo enemigo
    
        self.image = pygame.image.load("elementos/enemigo.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(ALTO // 2 - self.rect.height)
        #velocidad inicial
        self.velocidad_x = 5
        self.velocidad_y = 5

    def update(self):            
        #actualiza la posicion del enemigo
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        #limita el margen izquierdo
        if self.rect.left < 0:
            self.velocidad_x += 1

        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.velocidad_x -= 1


        #limita el margen arriba
        if self.rect.top < 0:
            self.velocidad_y += 1


        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.velocidad_y -= 1

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("elementos/ball.png"),(10,20))
        # self.image.set_colorkey()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x      

    def update(self):
        self.rect.y -= 15
        #se elimina la bala al llegar arriba
        if self.rect.bottom < 0:
            self.kill()  


pygame.init()
VENTANA = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("JUEGO DE NAVES")
clock = pygame.time.Clock()


sprites = pygame.sprite.Group()
enemigo_sprites = pygame.sprite.Group()
# disparo_sprites = pygame.sprite.Group()
balas = pygame.sprite.Group()

# for x in range(random.randrange(5) + 1):
enemigo = Enemigo()
enemigo_sprites.add(enemigo)

jugador = Jugador()
sprites.add(jugador)

# disparo = Disparo()
# disparo_sprites.add(disparo)

jugando = True
while jugando:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    sprites.update()
    enemigo_sprites.update()
    balas.update()

    explosion = pygame.sprite.spritecollide(jugador,enemigo_sprites,False)
    if explosion:
        enemigo.image = pygame.image.load("elementos/explosion.png")
        enemigo.velocidad_y += 7
    elif enemigo.rect.top > ALTO:
        enemigo.kill()


    VENTANA.fill(NEGRO)
    sprites.draw(VENTANA)
    enemigo_sprites.draw(VENTANA)
    balas.draw(VENTANA)

    pygame.display.flip()

pygame.quit()
