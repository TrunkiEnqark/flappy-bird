import pygame
from random import randint

# Const
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SCREEN_SCALE = (400, 600)
BIRD_SCALE = (35, 35)
d_2tube = 150
gravity = 0.5
FPS = 120 

# Variable
pygame.init()
screen = pygame.display.set_mode(SCREEN_SCALE)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
x_bird = 50
y_bird = 350
bird_drop_velocity = 0
tube1_x = 400
tube2_x = 600
tube3_x = 800
tube1_pass = False
tube2_pass = False
tube3_pass = False
tube_velocity = 2
tube_width = 40
tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)
score = 0
font = pygame.font.SysFont('san', 30)
font1 = pygame.font.SysFont('san', 40)
font2 = pygame.font.SysFont('san', 20)
running = True
pausing = False

# Load image
background_img = pygame.image.load('images/background.png')
bird_img = pygame.image.load('images/bird.png')
tube_img = pygame.image.load('images/tube.png')
tube_op_img = pygame.image.load('images/tube_op.png')
background_img = pygame.transform.scale(background_img, SCREEN_SCALE)
bird_img = pygame.transform.scale(bird_img, BIRD_SCALE)    

# Load Music
background_sound = pygame.mixer.Sound('audio/background-sound.mp3')
score_sound = pygame.mixer.Sound('audio/score.mp3')
fly_sound = pygame.mixer.Sound('audio/wing.mp3')

# Main code:
while running:
    pygame.mixer.Sound.play(background_sound)
    clock.tick(FPS)
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    
    tube1_img = pygame.transform.scale(tube_img, (tube_width, tube1_height))
    tube2_img = pygame.transform.scale(tube_img, (tube_width, tube2_height))
    tube3_img = pygame.transform.scale(tube_img, (tube_width, tube3_height))
    tube1 = screen.blit(tube1_img, (tube1_x, 0))
    tube2 = screen.blit(tube2_img, (tube2_x, 0))
    tube3 = screen.blit(tube3_img, (tube3_x, 0))
    
    tube1_op_img = pygame.transform.scale(tube_op_img, (tube_width, SCREEN_SCALE[1] - (tube1_height + d_2tube)))
    tube2_op_img = pygame.transform.scale(tube_op_img, (tube_width, SCREEN_SCALE[1] - (tube2_height + d_2tube)))
    tube3_op_img = pygame.transform.scale(tube_op_img, (tube_width, SCREEN_SCALE[1] - (tube3_height + d_2tube)))
    tube1_op = screen.blit(tube1_op_img, (tube1_x, tube1_height + d_2tube))
    tube2_op = screen.blit(tube2_op_img, (tube2_x, tube2_height + d_2tube))
    tube3_op = screen.blit(tube3_op_img, (tube3_x, tube3_height + d_2tube))
    
    tube1_x -= tube_velocity
    tube2_x -= tube_velocity
    tube3_x -= tube_velocity
    
    if tube1_x < -tube_width:
        tube1_x = SCREEN_SCALE[0] + 150
        tube1_height = randint(100, 400)
        tube1_pass = False
    
    if tube2_x < -tube_width:
        tube2_x = SCREEN_SCALE[0] + 150
        tube2_height = randint(100, 400)
        tube2_pass = False
    
    if tube3_x < -tube_width:
        tube3_x = SCREEN_SCALE[0] + 150
        tube3_height = randint(100, 400)
        tube3_pass = False
    
    bird = screen.blit(bird_img, (x_bird, y_bird))
    y_bird += bird_drop_velocity
    bird_drop_velocity += gravity
    
    score_txt = font.render("Score: " + str(score), True, RED)
    screen.blit(score_txt, (5, 5))
    
    if x_bird >= tube_width + tube1_x and tube1_pass == False:
        score += 1
        tube1_pass = True
    if x_bird >= tube_width + tube2_x and tube2_pass == False:
        score += 1
        tube2_pass = True
    if x_bird >= tube_width + tube3_x and tube3_pass == False:
        score += 1
        tube3_pass = True

    tubes = [tube1, tube2, tube3, tube1_op, tube2_op, tube3_op]
    for tube in tubes:
        if bird.colliderect(tube) or y_bird <= 0 or y_bird >= SCREEN_SCALE[1]:
            # pygame.mixer.pause()
            bird_drop_velocity = 0
            tube_velocity = 0  
            game_over_txt = font1.render("Game over", True, RED)
            score_txt = font1.render("Score: " + str(score), True, RED)
            space_txt = font2.render("Please enter Space to continue!", True, BLUE)
            screen.blit(game_over_txt, (100, 260))
            screen.blit(score_txt, (120, 290))
            screen.blit(space_txt, (70, 340))
            pausing = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(fly_sound)
                bird_drop_velocity = -7
                if pausing:
                    # pygame.mixer.unpause()
                    x_bird = 50
                    y_bird = 350
                    tube1_x = 400
                    tube2_x = 600
                    tube3_x = 800
                    tube_velocity = 2
                    score = 0
                    pausing = False
    pygame.display.flip() 
pygame.quit()