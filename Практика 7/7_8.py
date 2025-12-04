import pygame
import sys
import math
import numpy as np

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
GRAPH_COLOR = (0, 200, 255)
DERIVATIVE_COLOR = (255, 100, 0)
CURSOR_COLOR = (255, 255, 0)
TEXT_COLOR = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("График функции и её производной | Работа Павла Юнкер")
clock = pygame.time.Clock()

# Параметры графиков
x_min, x_max = -5, 5
y_min, y_max = -3, 3
cursor_x = 0  # Начальная позиция курсора

# Массив точек графика (изначально горизонтальная линия)
graph_points = [0.0] * WIDTH
dragging = False
drag_offset = 0.0

# Функция для преобразования математических координат в экранные
def math_to_screen(x, y, graph_height, offset_y):
    screen_x = int((x - x_min) / (x_max - x_min) * WIDTH)
    screen_y = int(offset_y - (y - y_min) / (y_max - y_min) * graph_height)
    return screen_x, screen_y

# Функция для преобразования экранных координат в математические
def screen_to_math(screen_x, screen_y, graph_height, offset_y):
    x = x_min + (screen_x / WIDTH) * (x_max - x_min)
    y = y_min + ((offset_y - screen_y) / graph_height) * (y_max - y_min)
    return x, y

# Функция f(x) - использует точки графика
def f(x):
    screen_x = int((x - x_min) / (x_max - x_min) * WIDTH)
    screen_x = max(0, min(WIDTH - 1, screen_x))
    return graph_points[screen_x]

# Производная функции f(x) - с пониженной точностью
def f_derivative(x):
    # Используем меньше точек для вычисления производной
    step = 5  # Берем точки через каждые 5 пикселей
    screen_x = (x - x_min) / (x_max - x_min) * WIDTH
    idx1 = (int(screen_x) // step) * step
    idx2 = min(idx1 + step, WIDTH - 1)
    
    if idx1 == idx2:
        return 0.0
    
    # Производная как разность между удаленными точками
    y1 = graph_points[idx1]
    y2 = graph_points[idx2]
    
    dx = (x_max - x_min) / WIDTH * step  # Увеличиваем dx
    derivative = (y2 - y1) / dx
    
    # Ограничиваем производную
    return max(-10, min(10, derivative))

# Отрисовка сетки
def draw_grid(graph_height, offset_y):
    # Вертикальные линии
    for x in range(int(x_min), int(x_max) + 1):
        if x != 0:
            screen_x, _ = math_to_screen(x, 0, graph_height, offset_y)
            pygame.draw.line(screen, GRID_COLOR, (screen_x, 0), (screen_x, HEIGHT), 1)
    
    # Горизонтальные линии
    for y in range(int(y_min), int(y_max) + 1):
        if y != 0:
            _, screen_y = math_to_screen(0, y, graph_height, offset_y)
            pygame.draw.line(screen, GRID_COLOR, (0, screen_y), (WIDTH, screen_y), 1)
    
    # Оси координат
    zero_x, _ = math_to_screen(0, 0, graph_height, offset_y)
    _, zero_y = math_to_screen(0, 0, graph_height, offset_y)
    pygame.draw.line(screen, (150, 150, 150), (zero_x, 0), (zero_x, HEIGHT), 2)
    pygame.draw.line(screen, (150, 150, 150), (0, zero_y), (WIDTH, zero_y), 2)

# Отрисовка графика функции
def draw_function(graph_height, offset_y, color):
    points = []
    for screen_x in range(WIDTH):
        x = x_min + (screen_x / WIDTH) * (x_max - x_min)
        try:
            y = f(x)
            if y_min <= y <= y_max:
                screen_y = int(offset_y - (y - y_min) / (y_max - y_min) * graph_height)
                points.append((screen_x, screen_y))
        except:
            continue
    
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 3)

# Отрисовка графика производной с пониженной точностью
def draw_derivative(graph_height, offset_y, color):
    points = []
    step = 3  # Рисуем точки только каждые 3 пикселя
    
    for screen_x in range(0, WIDTH, step):
        x = x_min + (screen_x / WIDTH) * (x_max - x_min)
        try:
            y = f_derivative(x)
            # Ограничиваем значения
            y = max(y_min, min(y_max, y))
            screen_y = int(offset_y - (y - y_min) / (y_max - y_min) * graph_height)
            points.append((screen_x, screen_y))
        except:
            continue
    
    if len(points) > 1:
        # Рисуем линию с более толстой линией для сглаживания
        pygame.draw.lines(screen, color, False, points, 2)

# Отрисовка вертикальной линии курсора
def draw_cursor_line(cursor_x, graph_height, offset_y):
    screen_x, _ = math_to_screen(cursor_x, 0, graph_height, offset_y)
    
    # Линия на верхнем графике
    y_value = f(cursor_x)
    if y_min <= y_value <= y_max:
        _, screen_y = math_to_screen(cursor_x, y_value, graph_height, offset_y)
        pygame.draw.line(screen, CURSOR_COLOR, (screen_x, 0), (screen_x, graph_height), 2)
        pygame.draw.circle(screen, CURSOR_COLOR, (screen_x, screen_y), 6)
    
    # Линия на нижнем графике
    derivative_value = f_derivative(cursor_x)
    if y_min <= derivative_value <= y_max:
        _, screen_y_deriv = math_to_screen(cursor_x, derivative_value, graph_height, offset_y + graph_height)
        pygame.draw.line(screen, CURSOR_COLOR, (screen_x, graph_height), (screen_x, HEIGHT), 2)
        pygame.draw.circle(screen, CURSOR_COLOR, (screen_x, screen_y_deriv), 6)

# Поиск ближайшей точки на графике для редактирования
def find_closest_point(mouse_x, mouse_y, graph_height, offset_y):
    min_distance = float('inf')
    closest_x = None
    
    for screen_x in range(WIDTH):
        x = x_min + (screen_x / WIDTH) * (x_max - x_min)
        y = f(x)
        if y_min <= y <= y_max:
            _, screen_y = math_to_screen(x, y, graph_height, offset_y)
            distance = abs(mouse_x - screen_x)
            
            # Проверяем расстояние до линии (по вертикали)
            if distance < 25 and abs(mouse_y - screen_y) < 25:  # Увеличили область захвата
                if distance < min_distance:
                    min_distance = distance
                    closest_x = screen_x
    
    return closest_x

# Редактирование графика с более широким воздействием
def edit_graph(mouse_x, mouse_y, graph_height, offset_y, start_drag=False):
    global graph_points, drag_offset
    
    if start_drag:
        closest_x = find_closest_point(mouse_x, mouse_y, graph_height, offset_y)
        if closest_x is not None:
            x = x_min + (closest_x / WIDTH) * (x_max - x_min)
            current_y = f(x)
            _, current_screen_y = math_to_screen(x, current_y, graph_height, offset_y)
            drag_offset = mouse_y - current_screen_y
            return closest_x
    else:
        closest_x = find_closest_point(mouse_x, mouse_y, graph_height, offset_y)
        if closest_x is not None:
            # Получаем новое значение Y
            new_screen_y = mouse_y - drag_offset
            _, new_y = screen_to_math(closest_x, new_screen_y, graph_height, offset_y)
            new_y = max(y_min, min(y_max, new_y))
            
            # Обновляем точку с более широким воздействием
            graph_points[closest_x] = new_y
            
            # Широкое сглаживание соседних точек
            for dx in range(-15, 16):  # Увеличили диапазон воздействия
                neighbor_x = closest_x + dx
                if 0 <= neighbor_x < WIDTH:
                    # Более плавное сглаживание для широких областей
                    weight = math.exp(-dx**2 / 50.0)  # Увеличили дисперсию для более широкого воздействия
                    current_val = graph_points[neighbor_x]
                    graph_points[neighbor_x] = current_val * (1 - weight) + new_y * weight
    
    return None

# Отрисовка информации
def draw_info(cursor_x, graph_height, offset_y):
    font = pygame.font.SysFont(None, 24)
    
    # Значения функции и производной
    y_value = f(cursor_x)
    derivative_value = f_derivative(cursor_x)
    
    # Текст для верхнего графика
    func_text = font.render(f"f({cursor_x:.2f}) = {y_value:.2f}", True, GRAPH_COLOR)
    screen.blit(func_text, (20, 20))
    
    # Текст для нижнего графика
    deriv_text = font.render(f"f'({cursor_x:.2f}) = {derivative_value:.2f}", True, DERIVATIVE_COLOR)
    screen.blit(deriv_text, (20, graph_height + 20))
    
    # Подписи графиков
    func_label = font.render("f(x) - редактируемый график", True, GRAPH_COLOR)
    deriv_label = font.render("f'(x) - производная (пониженная точность)", True, DERIVATIVE_COLOR)
    screen.blit(func_label, (WIDTH - 250, 20))
    screen.blit(deriv_label, (WIDTH - 300, graph_height + 20))
    
    # Инструкция
    instruction = font.render("Зажмите и тяните ЛЮБУЮ часть верхнего графика для редактирования", True, TEXT_COLOR)
    screen.blit(instruction, (WIDTH // 2 - 280, graph_height - 30))

# Основной цикл
running = True
dragging = False
current_drag_point = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                dragging = True
                mouse_x, mouse_y = event.pos
                graph_height = HEIGHT // 2
                # Проверяем, кликнули ли на верхний график
                if 0 <= mouse_y <= graph_height:
                    current_drag_point = edit_graph(mouse_x, mouse_y, graph_height, graph_height, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                current_drag_point = None
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            graph_height = HEIGHT // 2
            
            if dragging and current_drag_point is not None:
                # Редактируем график
                edit_graph(mouse_x, mouse_y, graph_height, graph_height, False)
            else:
                # Обновляем позицию курсора
                cursor_x, _ = screen_to_math(mouse_x, mouse_y, graph_height, graph_height)
                cursor_x = max(x_min, min(x_max, cursor_x))
    
    # Очистка экрана
    screen.fill(BACKGROUND_COLOR)
    
    # Высота каждого графика
    graph_height = HEIGHT // 2
    
    # Отрисовка сетки для обоих графиков
    draw_grid(graph_height, graph_height)  # Верхний график
    draw_grid(graph_height, graph_height * 2)  # Нижний график
    
    # Разделительная линия между графиками
    pygame.draw.line(screen, (100, 100, 100), (0, graph_height), (WIDTH, graph_height), 3)
    
    # Отрисовка графиков
    draw_function(graph_height, graph_height, GRAPH_COLOR)  # Верхний график - функция
    draw_derivative(graph_height, graph_height * 2, DERIVATIVE_COLOR)  # Нижний график - производная
    
    # Отрисовка курсора
    draw_cursor_line(cursor_x, graph_height, graph_height)
    
    # Отрисовка информации
    draw_info(cursor_x, graph_height, graph_height)
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
