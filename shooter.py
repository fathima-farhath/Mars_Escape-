import pygame
import os

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

#define player action variables
moving_left = False
moving_right = False
shoot =False

# load images
bullet_img=pygame.image.load('img/icons/bullet.png').convert_alpha()


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



class Soldier(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		

		animation_types = ['Idle', 'Run', 'Jump']
		for animation in animation_types:

			temp_list = []

			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def move(self, moving_left, moving_right):

		dx = 0
		dy = 0


		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1


		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True


		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y


		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False


		self.rect.x += dx
		self.rect.y += dy


	def update_animation(self):

		ANIMATION_COOLDOWN = 100

		self.image = self.animation_list[self.action][self.frame_index]

		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1

		if self.frame_index >= len(self.animation_list[self.action]):
			self.frame_index = 0



	def update_action(self, new_action):

		if new_action != self.action:
			self.action = new_action

			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y,direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed=10
		self.image=bullet_img
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.direction=direction
# creating sprite groups
bullet_group=pygame.sprite.Group()


player = Soldier('player', 200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 5)



run = True
while run:

	clock.tick(FPS)

	draw_bg()

	player.update_animation()
	player.draw()
	enemy.draw()
	# update and draw groups
	bullet_group.update()
	bullet_group.draw(screen)


	if player.alive:
		# shoot bullets
		if shoot:
			bullet=Bullet(player.rect.centerx+(player.rect.size[0]),player.rect.centery,player.direction)
			bullet_group.add(bullet)
		if player.in_air:
			player.update_action(2)
		elif moving_left or moving_right:
			player.update_action(1)
		else:
			player.update_action(0)
		player.move(moving_left, moving_right)


	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_UP and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False




	pygame.display.update()

pygame.quit()