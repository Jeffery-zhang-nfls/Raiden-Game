import pygame
import random
import math

#Initial interface
pygame.init()
screen = pygame.display.set_mode((800,600)) #size
pygame.display.set_caption("Jeffery's plane game") #program name
icon = pygame.image.load('UFO.png') #icon image
pygame.display.set_icon(icon)
BackgroundImg = pygame.image.load('Background.png') #background image

#Score
Score = 0
score_font = pygame.font.Font('freesansbold.ttf',32)

def show_score():
    score_text = f"Your score : {Score}"
    score_render = score_font.render(score_text,True,(255,255,255))
    screen.blit(score_render,(10,10))


#End
is_over = False
over_font = pygame.font.Font('freesansbold.ttf',64)

def check_is_over():
    if is_over:
        over_text = "Game Over"
        over_render = over_font.render(over_text,True,(255,255,255))
        screen.blit(over_render,(200,250))


#Plane
PlaneImg = pygame.image.load('Plane.png')
PlaneX = 400
PlaneY = 500
PlaneStep = 0 #plane's velocity

def move_plane():
    global PlaneX
    PlaneX += PlaneStep
    #prevent plane get out of bounds
    if PlaneX > 736:
        PlaneX = 736
    elif PlaneX < 0:
        PlaneX = 0

def control_plane():
    global running,PlaneStep
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #keyboard to control plane
        if event.type == pygame.KEYDOWN: #press the keyboard to move
            if event.key == pygame.K_RIGHT:
                PlaneStep = 8
            elif event.key == pygame.K_LEFT:
                PlaneStep = -8
            elif event.key == pygame.K_UP:
                bullets.append(Bullet())
        if event.type == pygame.KEYUP: #leave the keyboard to stop
            PlaneStep = 0


#Enemy
number_of_enemy = 6

class Enemy():
    def __init__(self):
        self.img = pygame.image.load('Enemy.png')
        self.x = random.randint(200,600)
        self.y = random.randint(50,150)
        self.step = random.randint(1,6)
    def reset(self):
        self.x = random.randint(200,600)
        self.y = random.randint(50,150)
        self.step = random.randint(1,6)

enemy = []
for i in range(number_of_enemy):
    enemy.append(Enemy())

def show_enemy():
    global is_over,Score
    for e in enemy:
        screen.blit(e.img,(e.x,e.y))
        e.x += e.step
        e.y += Score * 0.1
        if e.x > 736 or e.x < 0:
            e.step *= -1
            if e.y > 400:
                is_over = True
                print("Game over")
                enemy.clear()


#Distance
def distance(bx,by,ex,ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a*a + b*b)


#Bullet
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('Bullet.png')
        self.x = PlaneX + 16 #middle of plane in x
        self.y = PlaneY - 16 #head of plane in y
        self.step = 10
    #hit enemy
    def check_hit(self):
        global Score
        for e in enemy:
            if distance(self.x,self.y,e.x,e.y) < 30:
                bullets.remove(self)
                e.reset()
                Score += 1

bullets = []

def show_bullet():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y))
        b.check_hit()
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)


#Main loop
running = True
while running:
    screen.blit(BackgroundImg,(0,0))
    show_score()
    screen.blit(PlaneImg,(PlaneX,PlaneY))
    control_plane()
    move_plane()
    show_enemy()
    show_bullet()
    check_is_over()
    pygame.display.update()