# 2nd version
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (153, 24, 24)

# Цвет змейки
SNAKE_COLOR = (40, 138, 68)

# Цвет глаз змейки
EYES_COLOR = BORDER_COLOR

# Цвет шрифта
FONT_COLOR = (140, 18, 26)

# Скорость движения змейки:
SPEED = 10

# Шрифт
FONT_NAME = "SmallestPixel7.ttf"

# Файл фонового изображения
BG_IMAGE = "background.png"

# Флаг включения заставок
FEATURE_FLAG = False

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс описывает объекты игры. Абстрактный класс"""

    def __init__(self) -> None:
        self.position: tuple = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE,
        )
        self.body_color = None

    def draw(self) -> None:
        """Отрисовывает экземпляр класса."""
        pass


class Snake(GameObject):
    """Класс описывает объект игры змейку."""

    def __init__(self) -> None:
        super().__init__()
        self.length: int = 1
        self.positions: list = [self.position]
        self.direction: tuple[int, int] = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.body_color: tuple = SNAKE_COLOR
        self.eye_color: tuple = EYES_COLOR

    def update_direction(self) -> None:
        """Изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Движение змейки. Изменяет координаты элементов змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        self.position = (
            (self.position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (self.position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            del self.positions[-1]
        else:
            self.eye_color = (251, 255, 0)

    def draw(self) -> None:
        """Отрисовывает змейку."""
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        head_color = tuple(int(i - i * 0.25) for i in self.body_color)
        pygame.draw.rect(screen, head_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 2)
        eye1_pos = (
            (
                self.position[0]
                + [0.25, 0.75][self.direction in (RIGHT, DOWN)] * GRID_SIZE
            ),
            (
                self.position[1]
                + [0.25, 0.75][self.direction in (LEFT, DOWN)] * GRID_SIZE
            ),
        )
        eye2_pos = (
            (
                self.position[0]
                + [0.25, 0.75][self.direction in (RIGHT, UP)] * GRID_SIZE
            ),
            (
                self.position[1]
                + [0.25, 0.75][self.direction in (RIGHT, DOWN)] * GRID_SIZE
            ),
        )
        pygame.draw.circle(screen, self.eye_color, eye1_pos, 3)
        pygame.draw.circle(screen, self.eye_color, eye2_pos, 3)
        self.eye_color = EYES_COLOR

    def crash(self) -> None:
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (87, 2, 2), rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2)
            pygame.time.delay(20)
            pygame.display.update()

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змейки."""
        return self.position

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)
        self.positions = [self.position]
        self.length = 1


class Apple(GameObject):
    """Класс описывает объект игры яблоко."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: tuple = APPLE_COLOR

    def randomize_position(self, snake):
        """Задаёт случайную позицию яблоку."""
        while self.position in snake.positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key in (pygame.K_UP, pygame.K_w)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif (
                event.key in (pygame.K_DOWN, pygame.K_s)
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key in (pygame.K_LEFT, pygame.K_a)
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key in (pygame.K_RIGHT, pygame.K_d)
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def fade_in_out(fade_surface, background, is_fade_in=True) -> None:
    """Выполняет плавное затемнение-осветление экрана"""
    fade_dest = [(50, 200, 10), (200, 50, -10)][is_fade_in]
    for alpha in range(*fade_dest):
        screen.blit(background, (0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)


def show_text(text, size, x=SCREEN_WIDTH // 2,
              y=SCREEN_HEIGHT // 2, btn=False):
    """Формирует текстовые объекты для отображения на экране"""
    font = pygame.font.Font(FONT_NAME, size)
    text = font.render(text, True, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)
    if btn:
        return text_rect


def show_welcome(fade_surface, background, game_object):
    """Окно приветствия"""
    show_text("Питон", 160, y=SCREEN_HEIGHT // 3)
    show_text("Нажимай и погнали!", 50, y=SCREEN_HEIGHT // 3 * 2)
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                game_object.direction = UP
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                game_object.direction = DOWN
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                game_object.direction = LEFT
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            break
    fade_in_out(fade_surface, background)


def show_game_over(fade_surface, background, game_object):
    """Окно окончания игры"""
    fade_in_out(fade_surface, background, False)
    show_text("Игра окончена", 90, y=SCREEN_HEIGHT // 3)
    show_text(f"Яблок съедено - {game_object.length} шт",
              55, y=SCREEN_HEIGHT // 2)
    yes_btn = show_text(
        "Повторим!",
        25,
        x=SCREEN_WIDTH // 4,
        y=SCREEN_HEIGHT // 4 * 3,
        btn=True
    )
    no_btn = show_text(
        "Хватит, заканчиваем!",
        25,
        x=SCREEN_WIDTH // 3 * 2,
        y=SCREEN_HEIGHT // 4 * 3,
        btn=True,
    )
    pygame.display.update()
    action_not_chosen = True
    while action_not_chosen:  # Ожидание выбора действия повтор/выход
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_btn.collidepoint(event.pos):  # Нажат повтор
                    game_object.reset()
                    fade_in_out(fade_surface, background)
                    action_not_chosen = False
                    break
                if no_btn.collidepoint(event.pos):  # Нажат выход
                    pygame.quit()
                    raise SystemExit
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


def main():
    """Основной игровой цикл"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake)
    background = pygame.image.load(BG_IMAGE)
    background = pygame.transform.smoothscale(background, screen.get_size())
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    if FEATURE_FLAG:
        show_welcome(fade_surface, background, snake)
    while True:
        clock.tick(SPEED)
        screen.blit(background, (0, 0))
        snake.draw()
        apple.draw()
        handle_keys(snake)
        snake.move()
        pygame.display.update()
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake)
            snake.length += 1
        elif snake.get_head_position() in snake.positions[1:]:
            snake.crash()
            if FEATURE_FLAG:
                show_game_over(fade_surface, background, snake)
            else:
                break


if __name__ == "__main__":
    FEATURE_FLAG = True
    main()
