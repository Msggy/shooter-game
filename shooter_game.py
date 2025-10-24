from pygame import *
from random import randint

janela = display.set_mode((700, 500))
display.set_caption("catch-up")
background = transform.scale(image.load("sea.jpg"), (700, 500))

# musica de fundo
mixer.init()
mixer.music.load("ariel.mp3")
mixer.music.play()

game = True
clock = time.Clock()
FPS = 60


# classes sprites heroi
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, tamanho_x=110, tamanho_y=110):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (tamanho_x, tamanho_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        janela.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT] and self.rect.x < 610:
            self.rect.x += 10

    def fire(self):
        bala = Balas("tuba.png", self.rect.x, self.rect.y, 2, 135, 135)
        balas.add(bala)


class Inimigo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost += 1


class Lixo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost += 1


# classe das balas
class Balas(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.rect
            self.rect.y > 0
            lost += 1


som_balas = mixer.Sound("fire.ogg")
balas = sprite.Group()


heroi = Player("coral.png", 0, 380, 10, 140, 140)

inimigos = sprite.Group()
lixos = sprite.Group()
posicoes_inimigos = []
for i in range(2):
    posicao = randint(50, 650)
    inimigo = Inimigo("nemo.png", posicao, 0, randint(1, 2), 70, 60)
    inimigos.add(inimigo)
    posicoes_inimigos.append(posicao)

for i in range(1):
    posicao = randint(50, 650)
    if posicao in posicoes_inimigos:
        posicao += 10
    lixo = Lixo("lixo.png", posicao, 0, randint(1, 2), 70, 60)
    lixos.add(lixo)

# Variáveis
game = True
finish = False
nível = 1
lost = 0
killed = 0

# Texto
font.init()
texto = font.SysFont('Arial', 36)
texto_grande = font.SysFont('Arial', 76)
win = texto_grande.render("Ganhaste!", True, (8, 255, 230))
perdeste = texto_grande.render("Perdeste!", True, (8, 255, 230))


while game:
    if not finish:
        janela.blit(background, (0, 0))
        heroi.reset()
        heroi.update()
        balas.draw(janela)
        balas.update()
        inimigos.draw(janela)
        inimigos.update()
        lixos.draw(janela)
        lixos.update()
        texto_perder = texto.render("Perdeste:" + str(lost), 1, (227, 164, 16))
        janela.blit(texto_perder, (10, 20))
        texto_killed = texto.render("Atingidos:" + str(killed), 1, (227, 164, 16))
        janela.blit(texto_killed, (10, 50))

        if (
            sprite.spritecollide(heroi, inimigos, False)
            or lost >= 20
            or sprite.spritecollide(heroi, lixos, False)
        ):
            finish = True
            janela.blit(perdeste, (200, 200))

        collide = sprite.groupcollide(inimigos, balas, True, True)

        for e in collide:
            killed = killed + 1
            inimigo = Inimigo(
                "nemo.png", randint(80, 700 - 80), -40, randint(1, 2), 60, 70
            )
            inimigos.add(inimigo)

        if killed >= 22:
            finish = True
            janela.blit(win, (200, 200))

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                heroi.fire()
                som_balas.play()

    display.update()
    clock.tick(FPS)
