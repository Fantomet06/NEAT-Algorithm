from cgitb import small
import pygame
import random
import os
import sys

pygame.init()

screen_width = 1920
screen_heigth = 1080

screen = pygame.display.set_mode((screen_width, screen_heigth))

running = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

jumping = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

small_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

background = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

font = pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    x_pos = 80
    y_pos = 530
    jump_velocity = 8.5 #jump velocity

    def __init__(self, img=running[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.jump_velocity
        self.rect = pygame.Rect(self.x_pos, self.y_pos, img.get_width(), img.get_height())
        self.step_index = 0

    def update(self):
        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump() 

        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = jumping

        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel <= -self.jump_velocity:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.jump_velocity

    def run(self):
        self.image = running[self.step_index // 5]
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        #for obstacle in obstacles:
        #    pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)

class Obstacle:
    def __init__(self, image, num_of_cac) -> None:
        self.image = image
        self.type = num_of_cac
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width 

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 550


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 525

def remove(index):
    dinosaurs.pop(index)

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = [Dinosaur()]

    x_pos_bg = 0
    y_pos_bg = 600
    game_speed = 20

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render(f'Points:  {str(points)}', True, (0, 0, 0))
        screen.blit(text, (50, 50))

    def background_update():
        global x_pos_bg, y_pos_bg
        image_width = background.get_width()
        screen.blit(background, (x_pos_bg, y_pos_bg))
        screen.blit(background, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0, 0, 0))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(screen)

        if len(dinosaurs) == 0:
            break

        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(small_cactus, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(large_cactus, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect): 
                    remove(i)

        u_input = pygame.key.get_pressed()

        for i, dinosaur in enumerate(dinosaurs):
            if u_input[pygame.K_SPACE]:
                dinosaurs[i].dino_jump = True
                dinosaurs[i].dino_run = False

        background_update()
        score()
        clock.tick(30)
        pygame.display.update()

main()

    