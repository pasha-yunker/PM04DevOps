import pygame
import numpy as np
import math
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция жидкости с вращением | Работа Павла Юнкер")

# Цвета
BACKGROUND = (20, 20, 40)
GRID_COLOR = (50, 50, 80)
ACTIVE_COLOR = (0, 150, 255)
INACTIVE_COLOR = (30, 60, 90)
TEXT_COLOR = (200, 200, 255)

# Настройки сетки
GRID_SIZE = 20  # Количество квадратов в каждом направлении
SQUARE_SIZE = 30  # Размер каждого маленького квадрата
BIG_SQUARE_SIZE = GRID_SIZE * SQUARE_SIZE

# Положение большого квадрата
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Угол вращения (в радианах)
angle = 0
rotation_speed = 0.002

# Создаем поверхность для большого квадрата
big_square_surface = pygame.Surface((BIG_SQUARE_SIZE, BIG_SQUARE_SIZE), pygame.SRCALPHA)

# Функция для проверки, находится ли точка в нижней половине относительно угла
def is_in_bottom_half(x, y, angle_rad):
    # Преобразуем координаты в систему координат квадрата
    rel_x = x - BIG_SQUARE_SIZE // 2
    rel_y = y - BIG_SQUARE_SIZE // 2
    
    # Поворачиваем координаты обратно, чтобы выровнять с углом
    cos_angle = math.cos(-angle_rad)
    sin_angle = math.sin(-angle_rad)
    
    rotated_x = rel_x * cos_angle - rel_y * sin_angle
    rotated_y = rel_x * sin_angle + rel_y * cos_angle
    
    # Проверяем, находится ли точка в нижней половине
    return rotated_y > 0

# Функция для рисования сетки
def draw_grid(surface, current_angle):
    surface.fill((0, 0, 0, 0))  # Очищаем поверхность
    
    # Рисуем сетку
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = i * SQUARE_SIZE
            y = j * SQUARE_SIZE
            
            # Проверяем, находится ли квадрат в нижней половине
            center_square_x = x + SQUARE_SIZE // 2
            center_square_y = y + SQUARE_SIZE // 2
            
            if is_in_bottom_half(center_square_x, center_square_y, current_angle):
                color = ACTIVE_COLOR
            else:
                color = INACTIVE_COLOR
            
            # Рисуем квадрат
            pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(surface, GRID_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

# Создаем слайдер для управления углом
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.dragging = False
        self.handle_radius = 10
        
    def draw(self, surface):
        # Рисуем линию слайдера
        pygame.draw.rect(surface, GRID_COLOR, self.rect)
        
        # Рисуем ручку
        handle_x = self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.width
        handle_pos = (handle_x, self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surface, ACTIVE_COLOR, handle_pos, self.handle_radius)
        
        # Рисуем текст
        font = pygame.font.SysFont(None, 24)
        angle_text = f"Угол: {math.degrees(self.val):.1f}°"
        text_surface = font.render(angle_text, True, TEXT_COLOR)
        surface.blit(text_surface, (self.rect.x, self.rect.y - 30))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                handle_x = self.rect.x + (self.val - self.min) / (self.max - self.min) * self.rect.width
                handle_rect = pygame.Rect(handle_x - self.handle_radius, 
                                         self.rect.y + self.rect.height // 2 - self.handle_radius,
                                         self.handle_radius * 2, self.handle_radius * 2)
                
                if handle_rect.collidepoint(mouse_pos):
                    self.dragging = True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = pygame.mouse.get_pos()
                # Ограничиваем позицию мыши пределами слайдера
                mouse_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
                
                # Вычисляем новое значение
                self.val = self.min + (mouse_x - self.rect.x) / self.rect.width * (self.max - self.min)
                return True
        return False

# Создаем слайдер для управления углом
slider = Slider(100, HEIGHT - 50, WIDTH - 200, 20, -math.pi, math.pi, 0)

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обрабатываем события слайдера
        if slider.handle_event(event):
            angle = slider.val
    
    # Обновляем угол (автоматическое вращение)
    # angle += rotation_speed
    # slider.val = angle
    
    # Очищаем экран
    screen.fill(BACKGROUND)
    
    # Рисуем сетку на поверхности большого квадрата
    draw_grid(big_square_surface, angle)
    
    # Поворачиваем поверхность большого квадрата
    rotated_surface = pygame.transform.rotate(big_square_surface, math.degrees(angle))
    
    # Получаем новый прямоугольник для центрирования
    rotated_rect = rotated_surface.get_rect(center=(center_x, center_y))
    
    # Рисуем повернутую поверхность
    screen.blit(rotated_surface, rotated_rect)
    
    # Рисуем слайдер
    slider.draw(screen)
    
    # Рисуем инструкцию
    font = pygame.font.SysFont(None, 24)
    instruction = "Используйте слайдер для вращения квадрата"
    text_surface = font.render(instruction, True, TEXT_COLOR)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 20))
    
    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
