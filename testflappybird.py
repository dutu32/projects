import pygame
from pygame.locals import *

pygame.init()
clock=pygame.time.Clock()
fps=60
screen_width = 500
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

flying = False
gameover = False


#imagini
bg = pygame.image.load('bg.jpg')
ground_img = pygame.image.load('ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,3):
            img=pygame.image.load(f'bird{num}.png')
            self.images.append(img)

        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False

    def update(self):

        #------------------gravitatie------------------------
        if flying==True:
             self.vel+=0.5
        if self.vel>8:
            self.vel=8
        print(self.vel)
        if self.rect.bottom<550:

            self.rect.y+= int(self.vel)

        if gameover==False:
            #---------------------saritura------------------
            if pygame.key.get_pressed()[K_SPACE] and self.clicked==False:
                self.clicked=True
                self.vel=-10
            if not pygame.key.get_pressed()[K_SPACE]:
                self.clicked=False


        



            self.counter+=1
            flap_cooldown=5

            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            
    #---------------------animatie------------------
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90)
            self.vel=0



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('pipe.png')
        self.rect=self.image.get_rect()
        self.rect.topleft=[x,y]
        

        


bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
flappy=Bird(50,int(screen_height/2))
        
bird_group.add(flappy)








ground_scroll = 0
scroll_speed = 4


def draw_ground():
    screen.blit(ground_img, (ground_scroll, 550))
    screen.blit(ground_img, (ground_scroll + screen_width, 550))

#------------------PORNIRE JOC------------------------
run = True
while run:

    clock.tick(fps)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and flying == False  and gameover == False:
            flying = True

    if gameover==False:

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > screen_width:
            ground_scroll = 0

    
    screen.blit(bg, (0, 0))
    draw_ground()

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()


   #--------------------gameover------------------
    if flappy.rect.bottom>=550:
        gameover=True
        flying=False


    pygame.display.update()


pygame.quit()
