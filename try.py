import pygame
pygame.font.init()
pygame.mixer.init()

# ******setting************
WIDTH, HEIGHT = (900, 500)  # screen
WIDTH_SHIP, HEIGHT_SHIP = (40, 50)  # spaceship

BLACK = (0, 0, 0)  # black color
WHITE = (255, 255, 255)  # white color
RED = (255, 0, 0)  # red color
YELLOW = (255, 255, 0)  # yellow color

SPEED = 5  # speed of ship
BULLET_SPEED = 7 # speed of bullet
BULLET_MAX = 5 # max bullet in one time
FPS = 30  # FPS

# health font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)  # phong chu cho health
WINNER_FONT = pygame.font.SysFont('comicsans', 100)  # phong chu cho winner

# load pics
SCREEN_PIC = pygame.image.load('Assets/space.png')
YELLOW_SHIP_PIC = pygame.image.load('Assets/spaceship_yellow.png')
RED_SHIP_PIC = pygame.image.load('Assets/spaceship_red.png')

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
# ship
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_PIC, (WIDTH_SHIP, HEIGHT_SHIP)), 90)
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_PIC, (WIDTH_SHIP, HEIGHT_SHIP)), -90)

# Rectangle(x,y,width,height)
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)  # border rectangle
RED_REC = pygame.Rect(700, 300, WIDTH_SHIP, HEIGHT_SHIP)  # red ship rectangle
YELLOW_REC = pygame.Rect(100, 300, WIDTH_SHIP, HEIGHT_SHIP)  # yellow ship rectangle

# bullets
RED_BULLETS = []
YELLOW_BULLETS = []

# hit
YELLOW_HIT = pygame.USEREVENT + 1  # tao event moi, event ID
RED_HIT = pygame.USEREVENT + 2  # tao event moi, event ID

# dis play basic screen pygame
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# name of screen
pygame.display.set_caption('Ships Fire')
# *****Display screen******
def draw_Screen(RED_HEALTH, YELLOW_HEALTH):
    # display screen on picture out side
    SCREEN.blit(SCREEN_PIC, (0, 0))  # screen
    SCREEN.blit(YELLOW_SHIP, (YELLOW_REC.x, YELLOW_REC.y))  # yellow ship
    SCREEN.blit(RED_SHIP, (RED_REC.x, RED_REC.y))  # red ship
    # display border "draw by program"
    pygame.draw.rect(SCREEN, BLACK, BORDER)
    # display bullets
    for RED_BULLET in RED_BULLETS:
        pygame.draw.rect(SCREEN, RED, RED_BULLET)
    for YELLOW_BULLET in YELLOW_BULLETS:
        pygame.draw.rect(SCREEN, YELLOW, YELLOW_BULLET)
    # draw health
    red_health_text = HEALTH_FONT.render('health: ' + str(RED_HEALTH), True, WHITE)
    yellow_health_text = HEALTH_FONT.render('health: ' + str(YELLOW_HEALTH), True, WHITE)
    SCREEN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    SCREEN.blit(yellow_health_text, (10, 10))
    # update screen
    pygame.display.update()
#*********yellow move************
def yellow_move(keys_pressed):
    if keys_pressed[pygame.K_a] and YELLOW_REC.x > 0:  # left
        YELLOW_REC.x -= SPEED
    if keys_pressed[pygame.K_d] and YELLOW_REC.x + YELLOW_REC.width + 10 < BORDER.x:  # right
        YELLOW_REC.x += SPEED
    if keys_pressed[pygame.K_w] and YELLOW_REC.y > 0:  # up
        YELLOW_REC.y -= SPEED
    if keys_pressed[pygame.K_s] and YELLOW_REC.y + YELLOW_REC.height - 10 < HEIGHT:  # down
        YELLOW_REC.y += SPEED

def red_move(keys_pressed):
    if keys_pressed[pygame.K_LEFT] and RED_REC.x > BORDER.x + BORDER.width:  # left
        RED_REC.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and RED_REC.x + RED_REC.width + 10 < WIDTH:  # right
        RED_REC.x += SPEED
    if keys_pressed[pygame.K_UP] and RED_REC.y > 0:  # up
        RED_REC.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and RED_REC.y + RED_REC.height - 10 < HEIGHT:  # down
        RED_REC.y += SPEED

def fire():
    # yellow fire
    for YELLOW_BULLET in YELLOW_BULLETS:
        YELLOW_BULLET.x += BULLET_SPEED
        if RED_REC.colliderect(YELLOW_BULLET):
            pygame.event.post(pygame.event.Event(RED_HIT))
            YELLOW_BULLETS.remove(YELLOW_BULLET)
            BULLET_HIT_SOUND.play()
        elif YELLOW_BULLET.x > WIDTH:
            YELLOW_BULLETS.remove(YELLOW_BULLET)
    # red fire
    for RED_BULLET in RED_BULLETS:
        RED_BULLET.x -= BULLET_SPEED
        if YELLOW_REC.colliderect(RED_BULLET):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            RED_BULLETS.remove(RED_BULLET)
            BULLET_HIT_SOUND.play()
        elif RED_BULLET.x < 0:
            RED_BULLETS.remove(RED_BULLET)
def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, True, WHITE)
    SCREEN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)
# ******main program*******
def main():
    # khai bao thoi gian
    clock = pygame.time.Clock()
    # khai bao health
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    run = True
    while run:
        # khai bao toc do chay cua vong lap bang FPS
        clock.tick(FPS)
        # khai bao keyboard
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(YELLOW_BULLETS) < BULLET_MAX:
                    YELLOW_BULLET = pygame.Rect(YELLOW_REC.x + YELLOW_REC.width, YELLOW_REC.y + YELLOW_REC.height//2 - 9, 10, 6)
                    YELLOW_BULLETS.append(YELLOW_BULLET)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_KP3 and len(RED_BULLETS) < BULLET_MAX:
                    RED_BULLET = pygame.Rect(RED_REC.x, RED_REC.y + RED_REC.height//2 - 9, 10, 6)
                    RED_BULLETS.append(RED_BULLET)
                    BULLET_FIRE_SOUND.play()
                    # khai bao bi ban trung va mat mau
            # lost health
            if event.type == RED_HIT:
                RED_HEALTH -= 1
            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
        # khai bao tin nhan thang
        winner_text = ''
        if RED_HEALTH <= 0:
            winner_text = 'yellow win'
        if YELLOW_HEALTH <= 0:
            winner_text = 'red win'
        if winner_text != '':
            draw_winner(winner_text)
            break
        yellow_move(keys_pressed)
        red_move(keys_pressed)
        fire()
        draw_Screen(RED_HEALTH, YELLOW_HEALTH)
    pygame.quit()
if __name__ == '__main__':
    main()