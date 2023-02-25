import random
import time

import pygame
import sys

# Global variables for game
WIDTH = 1080
HEIGHT = 680
GAME_SPEED = 7
SPACE_SIZE = 40
SNAKE_BODY_LENGTH = 3
CACTUS_STARTUP_COUNT = 4

# colors
SCORE_COLOR = "#ffffff"
SNAKE_COLOR_HEAD = "#305223"
SNAKE_COLOR = "#4b733b"
BLACK_SCREEN = "#000000"
BOARD_COLOR = "#303634"
ORANGE = "#b58826"


class Snake:
    def __init__(self):
        self.body_length = SNAKE_BODY_LENGTH
        self.coordinates = []
        self.parts_of_body = []
        self.move_direction = 'down'
        self.score = 0

        for i in range(0, SNAKE_BODY_LENGTH):
            self.coordinates.append([0, SPACE_SIZE * SNAKE_BODY_LENGTH - i])
        for x, y in self.coordinates:
            square = pygame.draw.rect(screen, SNAKE_COLOR, [x, y, SPACE_SIZE, SPACE_SIZE])
            self.parts_of_body.append(square)

    def move(self, fruit, cactus):
        result = random.choice([True, False])
        x, y = self.coordinates[0]
        if self.move_direction == "up":
            y -= SPACE_SIZE
        elif self.move_direction == "down":
            y += SPACE_SIZE
        elif self.move_direction == "left":
            x -= SPACE_SIZE
        elif self.move_direction == "right":
            x += SPACE_SIZE
        self.coordinates.insert(0, (x, y))
        load_board()
        fruit.draw_fruit()
        cactus.draw_cactus()
        draw_score(self.score)
        square = pygame.draw.rect(screen, SNAKE_COLOR_HEAD, [x, y, SPACE_SIZE, SPACE_SIZE])
        self.parts_of_body.insert(0, square)
        for x, y in self.coordinates[1:]:
            square = pygame.draw.rect(screen, SNAKE_COLOR, [x, y, SPACE_SIZE, SPACE_SIZE])
            self.parts_of_body.insert(0, square)

        fruit_x, fruit_y = fruit.fruit_coordinates[0]
        if x == fruit_x and y == fruit_y:
            self.score += 1
            fruit_collected()
            fruit.update_position(cactus)
            if result:
                cactus.add_new_cactus()
        else:
            del self.coordinates[-1]
            del self.parts_of_body[-1]
        if snake_make_collision(self, cactus):
            game_over(self.score)

    def change_direction(self, direction):
        if direction == 'left':
            if self.move_direction != 'right':
                self.move_direction = direction

        elif direction == 'right':
            if self.move_direction != 'left':
                self.move_direction = direction

        elif direction == 'up':
            if self.move_direction != 'down':
                self.move_direction = direction

        elif direction == 'down':
            if self.move_direction != 'up':
                self.move_direction = direction


class DesertFruit:
    def __init__(self):
        self.fruit_coordinates = []
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.fruit_coordinates.insert(0, (x, y))

    def draw_fruit(self):
        x, y = self.fruit_coordinates[0]
        screen.blit(fruit_img, (x, y))

    def update_position(self, cactus):
        collision_flag = False
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        for x_cactus, y_cactus in cactus.cactus_coordinates:
            if x_cactus == x and y_cactus == y:
                collision_flag = True
        if collision_flag:
            self.update_position(cactus)
        else:
            self.fruit_coordinates.insert(0, (x, y))
            screen.blit(fruit_img, (x, y))


class Cactus:
    def __init__(self):
        self.cactus_coordinates = []
        for i in range(0, CACTUS_STARTUP_COUNT, 1):
            x = random.randint(1, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.cactus_coordinates.insert(0, (x, y))
            screen.blit(cactus_img, (x, y))

    def draw_cactus(self):
        for x, y in self.cactus_coordinates:
            screen.blit(cactus_img, (x, y))

    def add_new_cactus(self):
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.cactus_coordinates.insert(0, [x, y])


def snake_make_collision(snake, cactus):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True

    for x_cactus, y_cactus in cactus.cactus_coordinates:
        if x == x_cactus and y == y_cactus:
            return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def update_score_board(player_score, scores):
    for i in range(0, 3):
        if player_score > int(scores[i]):
            scores.insert(i, player_score)
            with open('../score.txt', 'w') as file:
                for j in range(0, 3):
                    file.write(str(scores[j]) + '\n')
            break


def print_score_board(score):
    scores = open_scores_files_and_read_it()
    font = pygame.font.Font(None, 74)
    text = "Twój wynik: " + str(score) + " pkt"
    text2 = "Trzy najlepsze wyniki:"
    text3 = "I miejsce:  " + str(scores[0]) + " pkt"
    text4 = "II miejsce:  " + str(scores[1]) + " pkt"
    text5 = "III miejsce: " + str(scores[2]) + " pkt"
    wybor = "Aby powrócić do menu głównego wciśnij ENTER, aby wyjść z gry wciśnij ESC"

    text_surface = font.render(text, True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 450))

    text_surface = font.render(text2, True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 150))

    text_surface = font.render(text3, True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 250))

    text_surface = font.render(text4, True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 310))

    text_surface = font.render(text5, True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 370))

    font = pygame.font.Font(None, 40)
    text_surface = font.render(wybor, True, ORANGE)
    text_width = text_surface.get_width()
    update_score_board(score, scores)
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 600))


def game_over(score):
    pygame.mixer.Channel(0).stop()
    pygame.mixer.music.load("../Resources/game_over.mp3")
    pygame.mixer.music.play()
    time.sleep(2)
    screen.fill("#000000")
    print_score_board(score)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        elif keys[pygame.K_RETURN]:
            break
    main_menu()
    snake_game()


def draw_score(score):
    font = pygame.font.Font(None, 74)
    text = "Wynik "
    text_surface = font.render(text + str(score), True, SCORE_COLOR)
    text_width = text_surface.get_width()
    screen.blit(text_surface, ((WIDTH - text_width) / 2, 15))


def fruit_collected():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("../Resources/fruit_collect.ogg"))


def draw_game_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, BOARD_COLOR, (1, x), (WIDTH, x), 2)
        pygame.draw.line(screen, BOARD_COLOR, (x, 1), (x, WIDTH), 2)


def open_scores_files_and_read_it():
    with open("../score.txt") as file:
        lines = [line.strip() for line in file]
    return lines


def load_menu():
    menu = pygame.image.load("../Resources/mainMenu.png")
    menu = pygame.transform.scale(menu, (WIDTH, HEIGHT))
    surf_center = (
        (WIDTH - menu.get_width()) / 2,
        (HEIGHT - menu.get_height()) / 2)
    screen.blit(menu, surf_center)


def load_board():
    image = pygame.image.load("../Resources/background.png")
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    surf_center = (
        (WIDTH - image.get_width()) / 2,
        (HEIGHT - image.get_height()) / 2)
    screen.blit(image, surf_center)


def main_menu():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('../Resources/mainSong.mp3'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        load_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        elif keys[pygame.K_SPACE]:
            break
        pygame.display.flip()
        clock.tick(10)


def snake_game():
    load_board()
    snake = Snake()
    fruit = DesertFruit()
    cactus = Cactus()
    while True:
        snake.move(fruit, cactus)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

        elif keys[pygame.K_UP]:
            snake.change_direction("up")
        elif keys[pygame.K_DOWN]:
            snake.change_direction("down")
        elif keys[pygame.K_LEFT]:
            snake.change_direction("left")
        elif keys[pygame.K_RIGHT]:
            snake.change_direction("right")
        draw_game_grid()
        draw_score(snake.score)

        pygame.display.flip()
        clock.tick(GAME_SPEED + int(snake.score / 2))


if __name__ == "__main__":
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DesertSnake")

    main_menu()

    fruit_img = pygame.image.load("../Resources/dragon-fruit.png")
    fruit_img = pygame.transform.scale(fruit_img, (40, 40))

    cactus_img = pygame.image.load("../Resources/cactus.png")
    cactus_img = pygame.transform.scale(cactus_img, (40, 40))

    snake_game()
