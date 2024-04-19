import pygame


pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 550
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
LIGHT_GREY = (192, 192, 192)
mw = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PingPong')

class Sprite:

    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_size):
        self.image = pygame.transform.scale(pygame.image.load(sprite_image).convert_alpha(), sprite_size)
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Racket(Sprite):

    points = 0

    def update_left(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 20:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.y < 375:
            self.rect.y += 5

    def update_right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 20:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.y < 375:
            self.rect.y += 5


class Ball(Sprite):

    def update_ball(self):
        if self.rect.x >= 860:
            racket_one.points += 1
            self.rect.x = 435
            self.rect.y = 255

        if self.rect.x <= -5:
            racket_two.points += 1
            self.rect.x = 435
            self.rect.y = 255


def render_score(racket): 
    result = ''
    if racket.points < 10:
        result = '0' + str(racket.points)
    else:
        result = str(racket.points)
    return number_font.render(result, True, LIGHT_GREY)


racket_one = Racket('white line.jpg', 20, 185, (20, 150))
racket_two = Racket('white line.jpg', 860, 185, (20, 150))
center = Sprite('grey line.png', 440, 0, (25, 550))
ball = Ball('ball.png', 435, 255, (40, 40))
ball_speed_x = 4
ball_speed_y = 4

number_font = pygame.font.Font('fonts//G7_Segment_7a.ttf', 100)
titule_font = pygame.font.Font('fonts//mc-ten-lowercase-alt.ttf', 80)
restart_font = pygame.font.Font('fonts//Pareidolia.ttf', 25)

winner_txt = titule_font.render('WINNER', True, WHITE)
loser_txt = titule_font.render('LOSER', True, LIGHT_GREY)
restart_txt = restart_font.render('RESTART', True, WHITE)

clock = pygame.time.Clock()
FPS = 60
game = True
finish = False

while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if not finish:

        mw.fill(BLACK)
        mw.blit(render_score(racket_one), (330, 23))
        mw.blit(render_score(racket_two), (480, 23))

        center.draw()
        ball.draw()
        racket_one.draw()
        racket_two.draw()
        border_one = pygame.draw.rect(mw, WHITE, pygame.Rect(0, 0, 900, 15))
        border_two = pygame.draw.rect(mw, WHITE, pygame.Rect(0, 535, 900, 15))

        racket_one.update_left()
        racket_two.update_right()
        ball.update_ball()

        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y

        if ball.rect.colliderect(border_one):
            ball_speed_y *= -1
        if ball.rect.colliderect(border_two):
            ball_speed_y *= -1
        if ball.rect.colliderect(racket_one.rect):
            ball_speed_x *= -1
        if ball.rect.colliderect(racket_two.rect):
            ball_speed_x *= -1

        if racket_one.points >= 10:
            mw.blit(winner_txt, (97, 190))
            finish = True
        elif racket_two.points == 10:
            mw.blit(loser_txt, (100, 190))

        if racket_two.points >= 10:
            mw.blit(winner_txt, (518, 190))
            finish = True
        elif racket_one.points == 10:
            mw.blit(loser_txt, (555, 190))
            
    else:
        rect_button = pygame.draw.rect(mw, WHITE, pygame.Rect(350, 400, 200, 100))
        main_button = pygame.draw.rect(mw, BLACK, pygame.Rect(357, 407, 186, 86))
        mw.blit(restart_txt, (372, 437))

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if main_button.collidepoint(x, y):
                finish = False
                racket_one.points = 0
                racket_two.points = 0
                racket_one.rect.x = 20
                racket_one.rect.y = 185
                racket_two.rect.x = 860
                racket_two.rect.y = 185

    clock.tick(FPS)
    pygame.display.update()