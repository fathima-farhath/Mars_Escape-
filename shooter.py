import pygame
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=int(SCREEN_WIDTH*0.6)
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption('Mars quit')

# Set frame rate
clock=pygame.time.Clock()
fps=60
# updating bg
def draw_bg():
    bg=(140,201,120)
    screen.fill(bg)

# Define playr action variables
move_left=False
move_right=False

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        self.direction=1
        self.flip=False
        img=pygame.image.load(f'img/{char_type}/0.png')
        self.image= pygame.transform.scale(img, (int(img.get_width() * 2.5), int(img.get_height() * 2.5)))
        self.rect=img.get_rect()
        self.rect.center=(x,y)
    def move(self,move_left,move_right):
        dx=0
        dy=0
        if move_left:
            dx=-self.speed
            self.direction=-1
            self.flip=True
        if move_right:
            dx=self.speed
            self.direction=1
            self.flip=False
        self.rect.x+=dx
        self.rect.y+=dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

player=Soldier('main_player',200,200,2)
# player1=Soldier(400,200)


run=True
while run:
    clock.tick(fps)
    draw_bg()
    player.draw()
    player.move(move_left,move_right)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        # key pressed
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                move_left=True
            if event.key==pygame.K_RIGHT:
                move_right=True
        # key released
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                move_left=False
            if event.key==pygame.K_RIGHT:
                move_right=False
            if event.key==pygame.K_ESCAPE:
                run=False

    pygame.display.update()
pygame.quit()