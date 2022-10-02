import pygame, sys, time, random


# Initialise game window
Screen_Width = 720
Screen_Height = 480

myScreen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Robogeneers Snake")


# Load assets
pSizeX = 20
pSizeY = 20

img1 = pygame.image.load("usercode/images/head.png").convert_alpha()
img_head = pygame.transform.scale(img1, (pSizeX, pSizeY))
imgRect_head = img_head.get_rect()

BODY_SCALE = 2  # this makes the body smaller than the head by a factor of BODY_SCALE
img2 = pygame.image.load("usercode/images/body.png").convert_alpha()
img_body = pygame.transform.scale(img2, (pSizeX/BODY_SCALE, pSizeY/BODY_SCALE))
imgRect_body = img_body.get_rect()

img3 = pygame.image.load("usercode/images/gear.png").convert_alpha()
img_gear = pygame.transform.scale(img3, (pSizeX, pSizeY))
imgRect_gear = img_gear.get_rect()

img4 = pygame.image.load("usercode/images/gameover.png").convert_alpha()
img_dead = pygame.transform.scale(img4, (200, 200))
imgRect_dead = img_dead.get_rect()
imgRect_dead.midtop = (Screen_Width/2, (Screen_Height)/3)


# Initialise game
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window object
game_window = pygame.display.set_mode((Screen_Width, Screen_Height))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
grey = pygame.Color(127, 127, 127)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS controller
fps_controller = pygame.time.Clock()


# Game variables
robot_loc = [100, 50]
body = [[0, 50], [100-10, 50], [100-(2*10), 50]]

gear_loc = [random.randrange(1, (Screen_Width//10)) * 10, random.randrange(1, (Screen_Height//10)) * 10]
gear_spawn = True

direction = 'RIGHT'
next_direction = direction

score = 0
start_speed = 15


# Game Over
def game_over():
    my_font = pygame.font.SysFont('Comic sans', 90)
    game_over_surface = my_font.render('GAME OVER', True, black)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (Screen_Width/2, Screen_Height/8)
    game_window.fill(green)
    game_window.blit(game_over_surface, game_over_rect)
    myScreen.blit(img_dead, imgRect_dead)
    show_score(0, black, 'times', 60)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    if choice == 1:
        score_surface = score_font.render(str(score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (Screen_Width/2, Screen_Height/3)
    else:
        score_surface = score_font.render('Score: ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (Screen_Width/2, Screen_Height/1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()


# Main logic
while True:

    ## MOVEMENT ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                next_direction = 'UP'
            if event.key == pygame.K_DOWN:
                next_direction = 'DOWN'
            if event.key == pygame.K_LEFT:
                next_direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                next_direction = 'RIGHT'
            # Quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the robot cannot move in the opposite direction instantaneously
    if next_direction == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if next_direction == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if next_direction == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if next_direction == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the robot
    if direction == 'UP':
        robot_loc[1] -= 10
    if direction == 'DOWN':
        robot_loc[1] += 10
    if direction == 'LEFT':
        robot_loc[0] -= 10
    if direction == 'RIGHT':
        robot_loc[0] += 10

    # robot body growing mechanism
    body.insert(0, list(robot_loc))
    if robot_loc[0] == gear_loc[0] and robot_loc[1] == gear_loc[1]:
        score += 1
        gear_spawn = False
    else:
        body.pop()

    # Spawning gears on the screen
    if not gear_spawn:
        gear_loc = [random.randrange(1, (Screen_Width//10)) * 10, random.randrange(1, (Screen_Height//10)) * 10]
    gear_spawn = True


    ## GFX ##
    # Alternate background every 5 points
    level = score // 5 + 1
    if level % 2:
        myScreen.fill(white)
    else:
        myScreen.fill(black)

    # Score
    show_score(1, grey, 'consolas', 100)

    # Level
    level_font = pygame.font.SysFont('consolas', 20)
    level_surface = level_font.render('Level ' + str(level), True, grey)
    level_rect = level_surface.get_rect()
    level_rect.midtop = (Screen_Width/2, Screen_Height/1.9)
    game_window.blit(level_surface, level_rect)

    # Gears
    myScreen.blit(img_gear, pygame.Rect(gear_loc[0], gear_loc[1], 10, 10))

    # Body
    for pos in body[1:]:
        myScreen.blit(img_body, pygame.Rect(pos[0] + pSizeX/(2*BODY_SCALE), pos[1] + pSizeY/(2*BODY_SCALE), 10, 10))

    # Head
    head_pos = body[0]
    myScreen.blit(img_head, pygame.Rect(head_pos[0], head_pos[1], 10, 10))

    # Update screen
    pygame.display.update()


    ## GAME OVER CONDITIONS ##
    # Getting out of bounds
    if robot_loc[0] < 0 or robot_loc[0] > Screen_Width-10:
        game_over()
    if robot_loc[1] < 0 or robot_loc[1] > Screen_Height-10:
        game_over()

    # Touching the robot body
    for block in body[1:]:
        if robot_loc[0] == block[0] and robot_loc[1] == block[1]:
            game_over()
    

    ## FRAME UPDATE ##
    # Refresh game screen
    pygame.display.update()

    # Refresh rate
    difficulty = start_speed + (level - 1) * 5
    fps_controller.tick(difficulty)
