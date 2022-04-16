import pygame
import os
pygame.font.init()
pygame.mixer.init()

# setting
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)  # phong chu cho health
WINNER_FONT = pygame.font.SysFont('comicsans', 100)  # phong chu cho winner
YELLOW_HIT = pygame.USEREVENT + 1  # tao event moi, event ID
RED_HIT = pygame.USEREVENT + 2  # tao event moi, event ID
BULLET_VEL = 7  # bullet velocity
MAX_BULLETS = 3  # maximum of bullets can fight
FPS = 30  # FPS
VEL = 5  # move
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (50, 40)
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# name of screen
pygame.display.set_caption('first game')
# color of screen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# Border
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)  # (x,y,width,height)

# ships
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
# ve ra toa do rectangle (red.x, red.y) va (yellow.x, yellow.y)
red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # (x,y,width,height)
yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # (x,y,width,height)
# display screen

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # den day man hinh voi mau trang
    WIN.blit(SPACE, (0, 0))
    # ve gioi han o giua man hinh
    pygame.draw.rect(WIN, BLACK, BORDER)
    # draw health
    red_health_text = HEALTH_FONT.render('health: ' + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render('health: ' + str(yellow_health), True, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # ve tau
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    # ve vien dan
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    # cap nhat man hinh
    pygame.display.update()

# dieu khien tau yellow
def yellow_handle_movement(keys_pressed):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT - 10:  # down
        yellow.y += VEL

# dieu khien tau red
def red_handle_movement(keys_pressed):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT - 10:  # down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH//2-2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

# main screen
def main():
    # khai bao dong ho thoi gian
    clock = pygame.time.Clock()
    # khai bao dan
    red_bullets = []
    yellow_bullets = []
    # khai bao health
    red_health = 10
    yellow_health = 10
    run = True
    while run:
        # khai bao toc do chay cua vong lap bang FPS
        clock.tick(FPS)
        # khai bao keyboard
        keys_pressed = pygame.key.get_pressed()
        # stop game
        for event in pygame.event.get():
            # nhan nut X goc phai man hinh de tat game
            if event.type == pygame.QUIT:
                run = False
            # nhan nut keydown de chon che do 2 nguoi choi
            if event.type == pygame.KEYDOWN:
                # khai bao bullet of yellow
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                # khai bao bullet of red
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 10, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            # khai bao bi ban trung va mat mau
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        # khai bao tin nhan thang
        winner_text = ''
        if red_health <= 0:
            winner_text = 'yellow win'
        if yellow_health <= 0:
            winner_text = 'red win'
        if winner_text != '':
            draw_winner(winner_text)
            break
        # cho tau yellow chay bang tay
        yellow_handle_movement(keys_pressed)
        red_handle_movement(keys_pressed)
        handle_bullets(yellow_bullets, red_bullets, red, yellow)
        # chay man hinh len
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # lenh tat game
    pygame.quit()
if __name__ == '__main__':
    main()