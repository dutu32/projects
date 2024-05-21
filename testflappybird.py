import pygame
from pygame.locals import *
import random

pygame.init()
clock=pygame.time.Clock()
fps=60
screen_width = 500
screen_height = 700


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')





#text
font=pygame.font.SysFont('Bauhaus 93',60)
#culoare
white=(255,255,255)


flying = False
gameover = False
pipe_gap = 250
pipe_frequency = 1500  #milisecunde
last_pipe = pygame.time.get_ticks() - pipe_frequency
score=0
pass_pipe=False



#imagini
bg = pygame.image.load('images/bg.jpg')
ground_img = pygame.image.load('images/ground.png')
button_img = pygame.image.load('images/reset.png')
button_img = pygame.transform.scale(button_img, (100, 100))
bird3=pygame.image.load('images/bird3.png')
bird3=pygame.transform.scale(bird3,(50,50))



#------------------scor display------------------------
def draw_text(text , font, text_col, x, y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))


#------------------reset---------------------
def reset_game():
    pipe_group.empty()
    flappy.rect.x=50
    flappy.rect.y=int(screen_height/2)
    score=0
    return score





class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,3):
            img=pygame.image.load(f'images/bird{num}.png')
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
        self.image=pygame.image.load('images/pipe.png')
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y- int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x,y + int(pipe_gap/2)]
        
    def update(self):
        self.rect.x-= scroll_speed
        if self.rect.right<0:
            self.kill()




class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
       

    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True            

        
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action


bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
flappy=Bird(50,int(screen_height/2))
        
bird_group.add(flappy)

button=Button(screen_width//2-50  ,screen_height//2-80,button_img)





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

    if gameover==False and flying==True:
        #---------------------creare tevi------------------
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-100,100) #---------pozitia tevilor

            btm_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,-1)
            top_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now




        ground_scroll -= scroll_speed
        if abs(ground_scroll) > screen_width:
            ground_scroll = 0
        pipe_group.update()

    
    screen.blit(bg, (0, 0))
    draw_ground()


#------------gameover reset------------------
    if gameover==True:
         if button.draw()==True:
                gameover=False
                score=reset_game()
                




    #---------------------scor------------------
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
            and pass_pipe==False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False
    
    draw_text(str(score),font,white,int(screen_width/2),20)
    









    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    

    #---------------lovituri-------------------
    if pygame.sprite.groupcollide(bird_group, pipe_group,False,False) or flappy.rect.top < 0:
        gameover=True
       






   #--------------------gameover------------------
    if flappy.rect.bottom>=550:
        gameover=True
        flying=False


    pygame.display.update()


pygame.quit()
