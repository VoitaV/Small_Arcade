import random
import pygame
import os

pygame.init()

clock = pygame.time.Clock()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption('PygameArcade')
score = 0
bulletSound = pygame.mixer.Sound("Game/bullet.wav")
hitSound = pygame.mixer.Sound("Game/hit.wav")
music = pygame.mixer.music.load("Game/music.mp3")
pygame.mixer.music.play(-1)
bg = pygame.image.load(os.path.join('Game', 'bg.jpg'))


class player(object):
    char = pygame.image.load(os.path.join('Game', 'standing.png'))
    walkRight = [
        pygame.image.load(os.path.join('Game', 'R1.png')), pygame.image.load(os.path.join('Game', 'R2.png')),
        pygame.image.load(os.path.join('Game', 'R3.png')), pygame.image.load(os.path.join('Game', 'R4.png')),
        pygame.image.load(os.path.join('Game', 'R5.png')), pygame.image.load(os.path.join('Game', 'R6.png')),
        pygame.image.load(os.path.join('Game', 'R7.png')), pygame.image.load(os.path.join('Game', 'R8.png')),
        pygame.image.load(os.path.join('Game', 'R9.png'))]
    walkLeft = [
        pygame.image.load(os.path.join('Game', 'L1.png')), pygame.image.load(os.path.join('Game', 'L2.png')),
        pygame.image.load(os.path.join('Game', 'L3.png')), pygame.image.load(os.path.join('Game', 'L4.png')),
        pygame.image.load(os.path.join('Game', 'L5.png')), pygame.image.load(os.path.join('Game', 'L6.png')),
        pygame.image.load(os.path.join('Game', 'L7.png')), pygame.image.load(os.path.join('Game', 'L8.png')),
        pygame.image.load(os.path.join('Game', 'L9.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:  # end of sprite loop
            self.walkCount = 0
        if not self.standing:
            if self.left:  # drawing walk left
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))  # chose sprite from the list
                self.walkCount += 1
            elif self.right:  # drawing walk right
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))  # chose sprite from the list
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(self.walkLeft[0], (self.x, self.y))
            else:
                win.blit(self.char, (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60  # We are resetting the player position
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [
        pygame.image.load(os.path.join('Game', 'R1E.png')), pygame.image.load(os.path.join('Game', 'R2E.png')),
        pygame.image.load(os.path.join('Game', 'R3E.png')), pygame.image.load(os.path.join('Game', 'R4E.png')),
        pygame.image.load(os.path.join('Game', 'R5E.png')), pygame.image.load(os.path.join('Game', 'R6E.png')),
        pygame.image.load(os.path.join('Game', 'R7E.png')), pygame.image.load(os.path.join('Game', 'R8E.png')),
        pygame.image.load(os.path.join('Game', 'R9E.png')), pygame.image.load(os.path.join('Game', 'R10E.png')),
        pygame.image.load(os.path.join('Game', 'R11E.png'))]
    walkLeft = [
        pygame.image.load(os.path.join('Game', 'L1E.png')), pygame.image.load(os.path.join('Game', 'L2E.png')),
        pygame.image.load(os.path.join('Game', 'L3E.png')), pygame.image.load(os.path.join('Game', 'L4E.png')),
        pygame.image.load(os.path.join('Game', 'L5E.png')), pygame.image.load(os.path.join('Game', 'L6E.png')),
        pygame.image.load(os.path.join('Game', 'L7E.png')), pygame.image.load(os.path.join('Game', 'L8E.png')),
        pygame.image.load(os.path.join('Game', 'L9E.png')), pygame.image.load(os.path.join('Game', 'L10E.png')),
        pygame.image.load(os.path.join('Game', 'L11E.png'))]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.jumpCountGoblin = 10
        self.isJump = False

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:  # end of sprite loop
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 50, 10))
        pygame.draw.rect(win, (10, 125, 10), (self.x, self.y - 20, 5 * self.health, 10))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def goblin_jump(self):
        if self.jumpCountGoblin >= -10:
            self.y -= (self.jumpCountGoblin * abs(self.jumpCountGoblin)) * 0.5  # jump trajectory
            self.jumpCountGoblin -= 1
        else:  # jump is finished
            self.jumpCountGoblin = 10
            self.isJump = False

    def move(self):
        if random.randint(1, 100) == 5 and not self.isJump:
            self.isJump = True

        if self.isJump:
            self.goblin_jump()

        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
            hitSound.play()
        else:
            goblin_list.pop(goblin_list.index(goblin))


def redrawGameWindow():
    global score
    win.blit(bg, (0, 0))  # draw our background image at (0,0)
    font = pygame.font.SysFont('comicsans', 30, True, True)
    text = font.render(f'Score: {score}', 1, (0, 0, 0))
    win.blit(text, (330, 10))
    man.draw(win)
    for goblin in goblin_list:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = player(50, 410, 64, 64)
bullets = []
goblin_list = []
# Main loop
run = True
while run:
    clock.tick(27)
    while len(goblin_list) < 2:
        goblin_list.append(enemy(random.randint(100, 400), 410, 64, 64, 450))
    for goblin in goblin_list:
        # if random.randint(1, 1000) == 10:
        #     enemy.goblin_jump(goblin)
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                    goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                        goblin.hitbox[3]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
            if 500 > bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # fire bullet
                if man.left:
                    facing = -1
                else:
                    facing = 1
                if len(bullets) < 5:
                    bulletSound.play()
                    bullets.append(
                        projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

    keys = pygame.key.get_pressed()
    # moved fire to events
    if keys[pygame.K_LEFT] and man.x - man.vel >= 0:  # move left
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x + man.vel + man.width <= 500:  # move right
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:  # not moving
        man.standing = True
        walkCount = 0
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5  # jump trajectory
            man.jumpCount -= 1
        else:  # jump is finished
            man.jumpCount = 10
            man.isJump = False

    redrawGameWindow()

pygame.quit()
