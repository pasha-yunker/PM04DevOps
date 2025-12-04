import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Интерактивный компас с магнитом | Работа Павла Юнкер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (200, 255, 200)
GRAY = (150, 150, 150)
DARK_RED = (180, 0, 0)
DARK_BLUE = (0, 0, 180)

# Параметры компаса
compass_radius = 70
compass_x, compass_y = WIDTH // 2, HEIGHT // 2
compass_dragging = False

# Параметры магнита
magnet_width = 180
magnet_height = 60
magnet_x, magnet_y = WIDTH // 4, HEIGHT // 2
magnet_dragging = False

# Функция для расчета позиций полюсов магнита
def get_magnet_poles():
    """
    Возвращает координаты полюсов магнита.
    Магнит расположен горизонтально:
    - ЛЕВАЯ половина: Северный полюс (N) - КРАСНЫЙ
    - ПРАВАЯ половина: Южный полюс (S) - СИНИЙ
    """
    # Северный полюс (красный) - центр левой стороны магнита
    north_pole_x = magnet_x - magnet_width // 2
    north_pole_y = magnet_y
    
    # Южный полюс (синий) - центр правой стороны магнита
    south_pole_x = magnet_x + magnet_width // 2
    south_pole_y = magnet_y
    
    return north_pole_x, north_pole_y, south_pole_x, south_pole_y

# Функция для расчета угла стрелки компаса
def calculate_needle_angle():
    """
    РАСЧЕТ УГЛА СТРЕЛКИ КОМПАСА:
    
    ФИЗИКА ВЗАИМОДЕЙСТВИЯ:
    - Северный полюс стрелки (КРАСНЫЙ) притягивается к Южному полюсу магнита (СИНИЙ)
    - Южный полюс стрелки (СИНИЙ) притягивается к Северному полюсу магнита (КРАСНЫЙ)
    
    УГОЛ РАССЧИТЫВАЕТСЯ КАК:
    Направление от компаса к южному полюсу магнита (синий полюс)
    Красный конец стрелки указывает на синий полюс магнита
    """
    north_pole_x, north_pole_y, south_pole_x, south_pole_y = get_magnet_poles()
    
    # Вектор от компаса к южному полюсу магнита (синему)
    # Красный конец стрелки указывает на синий полюс
    dx = south_pole_x - compass_x
    dy = south_pole_y - compass_y
    
    # Если полюс очень близко к компасу
    if dx == 0 and dy == 0:
        return 0
    
    # Угол в радианах - направление К синему полюсу магнита
    angle_rad = math.atan2(dy, dx)
    
    return angle_rad

# Функция для рисования треугольной стрелки
def draw_triangle_arrow(surface, color, start_pos, end_pos, size=15):
    """Рисует треугольную стрелку от start_pos к end_pos"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    # Вектор направления
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    
    if length == 0:
        return
    
    # Нормализуем вектор
    dx /= length
    dy /= length
    
    # Перпендикулярные векторы для основания треугольника
    perp_x = -dy * size
    perp_y = dx * size
    
    # Точки треугольника
    tip = (x2, y2)
    base1 = (x2 - dx * size + perp_x, y2 - dy * size + perp_y)
    base2 = (x2 - dx * size - perp_x, y2 - dy * size - perp_y)
    
    # Рисуем треугольник
    pygame.draw.polygon(surface, color, [tip, base1, base2])

# Функция для рисования компаса
def draw_compass(x, y, radius):
    """Рисует компас со стрелкой, ориентированной на магнит"""
    # Рисуем круг компаса
    pygame.draw.circle(screen, WHITE, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x, y), radius, 3)
    
    # Рисуем отметки сторон света
    font = pygame.font.SysFont(None, 28)
    directions = [("N", 0), ("E", 90), ("S", 180), ("W", 270)]
    
    for text, angle in directions:
        angle_rad = math.radians(angle)
        text_x = x + (radius - 20) * math.cos(angle_rad)
        text_y = y + (radius - 20) * math.sin(angle_rad)
        
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)
    
    # Рассчитываем угол для стрелки
    angle = calculate_needle_angle()
    
    # Рисуем стрелку
    # Красный конец указывает на южный полюс магнита (синий)
    red_end_x = x + radius * 0.8 * math.cos(angle)
    red_end_y = y + radius * 0.8 * math.sin(angle)
    
    # Синий конец указывает в противоположном направлении (на северный полюс)
    blue_end_x = x + radius * 0.8 * math.cos(angle + math.pi)
    blue_end_y = y + radius * 0.8 * math.sin(angle + math.pi)
    
    # Рисуем основную линию стрелки
    pygame.draw.line(screen, BLACK, (blue_end_x, blue_end_y), (red_end_x, red_end_y), 4)
    
    # Рисуем треугольные наконечники
    draw_triangle_arrow(screen, RED, (x, y), (red_end_x, red_end_y), 12)
    draw_triangle_arrow(screen, BLUE, (x, y), (blue_end_x, blue_end_y), 12)
    
    # Рисуем центр компаса
    pygame.draw.circle(screen, BLACK, (x, y), 8)

# Функция для рисования прямоугольного магнита
def draw_magnet(x, y, width, height):
    """Рисует горизонтальный магнит с цветными полюсами"""
    # Рисуем корпус магнита
    magnet_rect = pygame.Rect(x - width//2, y - height//2, width, height)
    pygame.draw.rect(screen, GRAY, magnet_rect)
    pygame.draw.rect(screen, BLACK, magnet_rect, 2)
    
    # Рисуем полюса магнита
    pole_width = width // 2
    north_pole = pygame.Rect(x - width//2, y - height//2, pole_width, height)
    south_pole = pygame.Rect(x, y - height//2, pole_width, height)
    
    pygame.draw.rect(screen, DARK_RED, north_pole)  # Северный полюс - КРАСНЫЙ
    pygame.draw.rect(screen, DARK_BLUE, south_pole) # Южный полюс - СИНИЙ
    
    # Подписи полюсов
    font = pygame.font.SysFont(None, 24)
    north_text = font.render("N", True, WHITE)
    south_text = font.render("S", True, WHITE)
    
    screen.blit(north_text, (x - width//2 + pole_width//2 - 5, y - 8))
    screen.blit(south_text, (x + pole_width//2 - 5, y - 8))

# Функция для отображения информации
def draw_info():
    """Отображает информацию о положении и взаимодействии"""
    font = pygame.font.SysFont(None, 24)
    

    
    # Угол стрелки
    angle = calculate_needle_angle()
    angle_deg = math.degrees(angle)
    angle_text = font.render(f"Угол стрелки: {angle_deg:.1f}°", True, BLACK)

    
    # Положение магнита относительно компаса
    rel_x = magnet_x - compass_x
    rel_y = magnet_y - compass_y
    
    position_text = font.render(f"Магнит относительно компаса: ({rel_x:.0f}, {rel_y:.0f})", True, BLACK)

    


# Функция проверки клика по магниту
def is_point_in_magnet(point_x, point_y, magnet_x, magnet_y, width, height):
    """Проверяет, находится ли точка внутри магнита"""
    return (magnet_x - width//2 <= point_x <= magnet_x + width//2 and 
            magnet_y - height//2 <= point_y <= magnet_y + height//2)

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка событий мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Проверяем, нажали ли на компас
            dist_to_compass = math.sqrt((mouse_x - compass_x)**2 + (mouse_y - compass_y)**2)
            if dist_to_compass <= compass_radius:
                compass_dragging = True
            
            # Проверяем, нажали ли на магнит
            if is_point_in_magnet(mouse_x, mouse_y, magnet_x, magnet_y, magnet_width, magnet_height):
                magnet_dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            compass_dragging = False
            magnet_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if compass_dragging:
                compass_x, compass_y = pygame.mouse.get_pos()
            elif magnet_dragging:
                magnet_x, magnet_y = pygame.mouse.get_pos()
    
    # Отрисовка
    screen.fill(GRAY)
    
    # Рисуем компас и магнит
    draw_compass(compass_x, compass_y, compass_radius)
    draw_magnet(magnet_x, magnet_y, magnet_width, magnet_height)
    
    # Отображаем информацию
    draw_info()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
