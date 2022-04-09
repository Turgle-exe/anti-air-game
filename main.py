# imports for game please instal libraries with (FILE NAME HERE.py)
import pygame
import random
import time
import sys
import os

global lives

# The Initiation function to load pygame in  EVERY pygame script
pygame.init()
# RGB color values
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
bright_green = (0, 255, 0)
orange = (255, 165, 0)
# with and hight for game DONT CHANGE
display_width = 1920
display_height = 900
# Clock for setting speed
clock = pygame.time.Clock()
# sprite groups for explosions and plane
explosion_sprite = pygame.sprite.Group()
plane_sprites = pygame.sprite.Group()

# creates display and loads images that are useed in game (change for funny thing but keep original images)
gameDisplay = pygame.display.set_mode((display_width, display_height))

backgound_image = pygame.image.load('city_background.jpg')
plane_image = pygame.image.load('plane.png')
plane_image.set_colorkey(black)
crosshair_image = pygame.image.load('crosshair.png')
explosion1 = pygame.image.load('explosion1.png')
explosion1.set_colorkey(black)
explosion2 = pygame.image.load('explosion2.png')
explosion2.set_colorkey(black)
explosion4 = pygame.image.load('explosion4.png')
explosion4.set_colorkey(black)
explosion3 = pygame.image.load('explosion3.png')
explosion3.set_colorkey(black)
explosion5 = pygame.image.load('explosion5.png')
explosion5.set_colorkey(black)
explosion6 = pygame.image.load('explosion6.png')
explosion1.set_colorkey(black)
exploded_image = pygame.image.load('dead.png')


# blueprint for plane sprites
class Plane(pygame.sprite.Sprite):
    # takes an x and y intiger coredinates for where to put the sprite uses as CENTER not top left
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = plane_image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # Updates the x position of the plane sprite by v the velosity
    def update(self, v):
        self.x -= v
        self.rect.center = [self.x, self.y]
        if self.x == -50:
            self.image = exploded_image
            self.kill()


class Plane_destroyed(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        super().__init__()
        self.x = x
        self.y = y
        self.t = t
        self.image = exploded_image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self, v):
        self.t += 1
        if self.t >= 30:
            self.kill()







# displays croshair image with x and y arguments
def crosshair(x, y):
    gameDisplay.blit(crosshair_image, (x, y))


# Displays explosion animation under croshair
class Explosion(pygame.sprite.Sprite):
    # creates instance of an explosion centered on x and y intiger arguments
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__()
        self.exploding_animation = False
        self.sprites = []
        self.sprites.append(explosion1)
        self.sprites.append(explosion2)
        self.sprites.append(explosion3)
        self.sprites.append(explosion4)
        self.sprites.append(explosion5)
        self.sprites.append(explosion6)
        self.sprites.append(explosion6)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # on update the current sprite increses by .2
    # it is then cast into an int witch causes the frame of the animation to update every 5 game ticks
    def update(self, v):
        self.current_sprite += .2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]


# displays the amount of lives
# the player has in top left corner
def life(count):
    font = pygame.font.SysFont("calibri", 40)
    text = font.render(f'Lives: {str(count)}', True, (150, 67, 37))
    gameDisplay.blit(text, (0, 0))


# Displayes cooldown for next shot in the top right corner
def display_cooldown(cooldown):
    font = pygame.font.SysFont("calibri", 40)
    cooldown = 30 - cooldown
    text = font.render(f'Cooldown: {str(cooldown // 5)}', True, (150, 67, 37))
    gameDisplay.blit(text, (1700, 0))


# displayes what level the player is currently on top middle of the game
def Level(count):
    font = pygame.font.SysFont("calibri", 40)
    text = font.render(f'level: {str(count)}', True, (150, 67, 37))
    gameDisplay.blit(text, (900, 0))


# Takes text and font strings and renders them to the TextSurface variable
# returns both textsurface's and textsurface's rectangle
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


''' function for creating button that runs other function
arguments are:
msg for the string to display on button
x for x position and y for y position
w for with and h for height
ic for color when mouse not hovering on it
ac for color when mouse is hovering on it
action is the function that the button executes when presses
'''


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont('calibri', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


# when ran kills program x_x
def quitgame():
    pygame.quit()
    quit()


# displys the intro with quit and replay buttons
def intro():
    intro = True
    pygame.mouse.set_visible(True)

    while intro:
        gameDisplay.blit(backgound_image, (0, 0))
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        largeText = pygame.font.SysFont('calibri', 115)
        TextSurf, TextRect = text_objects('Anti Air Anarchy', largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 600, 600, 100, 50, green, bright_green, game_loop)
        button("STOP!", 1200, 600, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


# the mainframe
def game_loop():
    # declare needed variables for game change for funny effects
    # DONT CHANGE THES
    pygame.mouse.set_visible(False)
    clicked = False
    total_planes_spawned = 0
    planes_destroyed = 0
    spawned_planes = 0
    tick = 0
    # you can change these (ptnl is planes untill next level)
    cooldown = 30
    level = 1
    lives = 3
    ptnl = 15
    # infinite loop for mainframe
    while True:
        # keeps track of frames since last plane was spawned
        tick += 1
        # displayes backround image
        gameDisplay.blit(backgound_image, (0, 0))
        life(lives)
        Level(level)
        # keeps track of ticks since last shot
        cooldown += 1
        # gets where mouse is and if its clicked
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # for loop for event handling such as a key press
        for event in pygame.event.get():
            # closes program if x button is pressed on screen
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # runs cooldown function and displays counter when cooldown less than 30
        if cooldown < 30:
            display_cooldown(cooldown)

        # determinzs the plane spawning rate based on level and spawns plane
        if tick == 150 // level:
            plane_sprites.add(Plane(1920, random.randint(60, 840)))
            tick = 0
            spawned_planes += 1
            total_planes_spawned += 1
        # when next level happens the are 5 planes added to the planes to next level and spawned planes is reset
        if spawned_planes == ptnl:
            level += 1
            ptnl += 5
            spawned_planes = 0
        # when a plane is removed from plane sprites it deletes a life planes destroyed
        if len(plane_sprites.sprites()) < total_planes_spawned:
            lives -= 1
            total_planes_spawned += 1
        # when there is no lmb input the clicked variable is set to False
        if not click[0]:
            clicked = False
        # if statment to create a sprite where the mouse is
        if click[0] and not clicked and cooldown >= 30:
            explosion = Explosion(mouse[0], mouse[1])
            explosion_sprite.add(explosion)
            clicked = True
            cooldown = 0
            # loops through every sprite  in the plane party yacht
            for p in plane_sprites.sprites():
                # destroys plane if explosion is within size of plane texture
                if p.x - 97 <= mouse[0] <= p.x + 97 + 134 and p.y - 97 <= mouse[1] <= p.y + 97:
                    p.kill()
                    exploded = Plane_destroyed(p.x, p.y, 15)
                    explosion_sprite.add(exploded)
                    total_planes_spawned -= 1
        # draws sprites from party yachts
        plane_sprites.draw(gameDisplay)
        explosion_sprite.draw(gameDisplay)

        plane_sprites.update(5)
        explosion_sprite.update(5)

        # removes explosion from party yacht after completed animation
        if explosion.current_sprite >= 6:
            explosion_sprite.remove(explosion)
        # resets game when you run out of Lives
        if lives == 0:
            plane_sprites.empty()
            explosion_sprite.empty()
            intro()
        # crosshair displays at mouse location
        crosshair(mouse[0] - 50, mouse[1] - 50)
        # random stuff idk just wright it
        pygame.display.update()
        clock.tick(60)


'''
wow
300 lines
...
not filling space
...
nope
yea 300 line code
'''
# game run
intro()
