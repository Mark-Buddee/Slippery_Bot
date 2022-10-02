import pygame, sys, time, random


# Initialise game window
frame_size_x = 720
frame_size_y = 480

myScreen = pygame.display.set_mode((frame_size_x, frame_size_y))
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

img3 = pygame.image.load("usercode/images/food.png").convert_alpha()
img_food = pygame.transform.scale(img3, (pSizeX, pSizeY))
imgRect_food = img_food.get_rect()

img4 = pygame.image.load("usercode/images/gameover.png").convert_alpha()
img_dead = pygame.transform.scale(img4, (200, 200))
imgRect_dead = img_dead.get_rect()
imgRect_dead.midtop = (frame_size_x/2, (frame_size_y)/3)


# Initialise game
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window object
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


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
snake_pos = [100, 50]
snake_body = [[0, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
start_speed = 15


# Game Over
def game_over():
    my_font = pygame.font.SysFont('Comic sans', 90)
    game_over_surface = my_font.render('GAME OVER', True, black)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/8)
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
        score_rect.midtop = (frame_size_x/2, frame_size_y/3)
    else:
        score_surface = score_font.render('Score: ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
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
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True


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
    level_rect.midtop = (frame_size_x/2, frame_size_y/1.9)
    game_window.blit(level_surface, level_rect)

    # Food
    myScreen.blit(img_food, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Body
    for pos in snake_body[1:]:
        myScreen.blit(img_body, pygame.Rect(pos[0] + pSizeX/(2*BODY_SCALE), pos[1] + pSizeY/(2*BODY_SCALE), 10, 10))

    # Head
    head_pos = snake_body[0]
    myScreen.blit(img_head, pygame.Rect(head_pos[0], head_pos[1], 10, 10))

    # Update screen
    pygame.display.update()


    ## GAME OVER CONDITIONS ##
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    

    ## FRAME UPDATE ##
    # Refresh game screen
    pygame.display.update()

    # Refresh rate
    difficulty = start_speed + (level - 1) * 5
    fps_controller.tick(difficulty)




## UNUSED CODE ##
    # pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    # xy-coordinate -> .Rect(x, y, size_x, size_y)
    # .draw.rect(play_surface, color, xy-coordinate)
    # pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    # myScreen.blit(img_head, imgRect_head)
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors