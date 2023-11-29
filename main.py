import pygame
import os
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption('TechWithTimLessons')

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
bg = pygame.image.load(os.path.join('Game', 'bg.jpg'))
char = pygame.image.load(os.path.join('Game', 'standing.png'))


class player(object):
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

    def draw(self, win):
        if self.walkCount + 1 >= 27:  # end of sprite loop
            self.walkCount = 0
        if not self.standing:
            if self.left:  # drawing walk left
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))  # chose sprite from the list
                self.walkCount += 1
            elif self.right:  # drawing walk right
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))  # chose sprite from the list
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(char, (self.x, self.y))


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
        self.path = [self.x, self.x]
        self.walkCount = 0
        self.vel = 3

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

    def move(self):
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


def redrawGameWindow():

    win.blit(bg, (0, 0))  # draw our background image at (0,0)
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = player(200, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
# Main loop
run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0, 0, 0), facing))
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
            # man.right = False
            # man.left = False
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
