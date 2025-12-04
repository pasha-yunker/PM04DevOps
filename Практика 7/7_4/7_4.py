import pygame
import sys
import math
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 600
FPS = 60
BACKGROUND_COLOR = (150, 150, 150)
WIRE_COLOR = (100, 100, 100)
PARTICLE_COLOR = (0, 100, 255)
RESISTOR_PARTICLE_COLOR = (255, 100, 0)
TEXT_COLOR = (255, 255, 255)
BATTERY_COLOR = (200, 200, 0)
RESISTOR_COLOR = (150, 75, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движение заряженных частиц в цепи | Работа Павла Юнкер")
clock = pygame.time.Clock()

# Инициализация шрифтов
font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 36)

# Класс для частиц, движущихся по контуру
class WireParticle:
    def __init__(self, start_distance):
        self.distance = start_distance  # Расстояние от начала пути
        self.speed = 0
        self.radius = 4
        self.color = PARTICLE_COLOR
    
    def update(self, voltage):
        # Скорость пропорциональна напряжению
        self.speed = abs(voltage) * 0.8
        
        # Двигаем частицу вперед
        if voltage >= 0:
            self.distance += self.speed
        else:
            self.distance -= self.speed
        
        # Зацикливаем расстояние по всей длине пути
        total_length = self.get_total_length()
        if self.distance >= total_length:
            self.distance -= total_length
        elif self.distance < 0:
            self.distance += total_length
    
    def get_total_length(self):
        """Общая длина всего пути"""
        # Длина всех сегментов: верхний провод + левый вертикальный + нижний провод + правый вертикальный
        return (WIDTH - 50 - 110) + (HEIGHT // 2 - 150) + (WIDTH - 50 - 110) + (HEIGHT // 2 - 150)
    
    def get_coordinates(self, voltage):
        """Получить координаты частицы на основе пройденного расстояния"""
        battery_x = WIDTH // 2 - 60
        battery_y = 100
        battery_width = 120
        battery_height = 60
        
        total_length = self.get_total_length()
        current_distance = self.distance % total_length
        
        # Определяем сегменты пути
        segment1_length = WIDTH - 50 - 110  # Верхний горизонтальный провод
        segment2_length = HEIGHT // 2 - 150  # Левый вертикальный провод
        segment3_length = WIDTH - 50 - 110  # Нижний горизонтальный провод  
        segment4_length = HEIGHT // 2 - 150  # Правый вертикальный провод
        
        if voltage >= 0:
            # Движение от плюса к минусу (против часовой стрелки)
            if current_distance < segment1_length:
                # Верхний горизонтальный провод (справа налево)
                x = WIDTH - 50 - current_distance
                y = HEIGHT // 2
            elif current_distance < segment1_length + segment2_length:
                # Левый вертикальный провод (ВВЕРХ - инвертировано)
                dist_in_segment = current_distance - segment1_length
                x = 110
                y = ((battery_y + battery_height // 2) - dist_in_segment) - 150  # ← ИНВЕРТИРОВАНО: было +, стало -
            elif current_distance < segment1_length + segment2_length + segment3_length:
                # Нижний горизонтальный провод (слева направо)
                dist_in_segment = current_distance - segment1_length - segment2_length
                x = 110 + dist_in_segment
                y = battery_y + battery_height // 2
            else:
                # Правый вертикальный провод (ВНИЗ - инвертировано)
                dist_in_segment = current_distance - segment1_length - segment2_length - segment3_length
                x = WIDTH - 50
                y = 150 + dist_in_segment  # ← ИНВЕРТИРОВАНО: было -, стало +
        else:
            # Движение от плюса к минусу (по часовой стрелке)
            if current_distance < segment1_length:
                # Верхний горизонтальный провод (слева направо)
                x = 110 + current_distance
                y = HEIGHT // 2
            elif current_distance < segment1_length + segment2_length:
                # Правый вертикальный провод (ВВЕРХ - инвертировано)
                dist_in_segment = current_distance - segment1_length
                x = WIDTH - 50
                y = ((battery_y + battery_height // 2) - dist_in_segment) - 150  # ← ИНВЕРТИРОВАНО: было +, стало -
            elif current_distance < segment1_length + segment2_length + segment3_length:
                # Нижний горизонтальный провод (справа налево)
                dist_in_segment = current_distance - segment1_length - segment2_length
                x = WIDTH - 50 - dist_in_segment
                y = battery_y + battery_height // 2
            else:
                # Левый вертикальный провод (ВНИЗ - инвертировано)
                dist_in_segment = current_distance - segment1_length - segment2_length - segment3_length
                x = 110
                y = (HEIGHT // 2 + dist_in_segment) - 150  # ← ИНВЕРТИРОВАНО: было -, стало +
        
        return int(x), int(y)
    
    def draw(self, voltage):
        x, y = self.get_coordinates(voltage)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)

# Класс для частиц в резисторе
class ResistorParticle:
    def __init__(self, x, y):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.amplitude = 0
        self.frequency = random.uniform(0.05, 0.1)
        self.phase = random.uniform(0, 2 * math.pi)
        self.radius = 4
        self.color = RESISTOR_PARTICLE_COLOR
    
    def update(self, speed):
        # Амплитуда колебаний пропорциональна скорости частиц в проводе
        self.amplitude = abs(speed) * 0.3
        
        # Колебательное движение
        self.x = self.original_x + math.sin(pygame.time.get_ticks() * self.frequency + self.phase) * self.amplitude
        self.y = self.original_y + math.cos(pygame.time.get_ticks() * self.frequency + self.phase) * self.amplitude
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Класс для трекбара
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x + (initial - min_val) / (max_val - min_val) * width - 5, 
                                      y - 5, 10, height + 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.dragging = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.value = self.min_val + (self.handle_rect.x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
    
    def draw(self):
        # Отрисовка трекбара
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.handle_rect)
        
        # Отображение значения
        text = font.render(f"Напряжение: {self.value:.1f} В", True, TEXT_COLOR)
        screen.blit(text, (self.rect.x, self.rect.y - 30))

# Создание объектов
wire_particles = []
resistor_particles = []

# Создание частиц с равномерным распределением по всему проводу
num_particles = 60
total_length = (WIDTH - 50 - 110) * 2 + (HEIGHT // 2 - 150) * 2
spacing = total_length / num_particles

for i in range(num_particles):
    start_distance = i * spacing
    wire_particles.append(WireParticle(start_distance))

# Создание частиц в резисторе
for i in range(8):
    for j in range(5):
        x = WIDTH // 2 - 50 + i * 15
        y = HEIGHT // 2 - 30 + j * 15
        resistor_particles.append(ResistorParticle(x, y))

# Создание трекбара
voltage_slider = Slider(100, HEIGHT - 50, WIDTH - 200, 20, -10, 10, 0)

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        voltage_slider.handle_event(event)
    
    # Очистка экрана
    screen.fill(BACKGROUND_COLOR)
    
    # Координаты батарейки
    battery_x = WIDTH // 2 - 60
    battery_y = 100
    battery_width = 120
    battery_height = 60
    
    # Отрисовка полного контура провода ПОД батарейкой
    
    # Верхний горизонтальный провод (основной)
    pygame.draw.line(screen, WIRE_COLOR, (110, HEIGHT // 2), (WIDTH - 50, HEIGHT // 2), 5)
    
    # Правый вертикальный провод (от нижнего провода к верхнему)
    pygame.draw.line(screen, WIRE_COLOR, (WIDTH - 50, battery_y + battery_height // 2), (WIDTH - 50, HEIGHT // 2), 5)
    
    # Левый вертикальный провод (от верхнего провода к нижнему)
    pygame.draw.line(screen, WIRE_COLOR, (110, HEIGHT // 2), (110, battery_y + battery_height // 2), 5)
    
    # Нижний горизонтальный провод (под батарейкой)
    pygame.draw.line(screen, WIRE_COLOR, (110, battery_y + battery_height // 2), (WIDTH - 50, battery_y + battery_height // 2), 5)
    
    # Отрисовка резистора (на верхнем проводе)
    resistor_x = WIDTH // 2 - 80
    resistor_y = HEIGHT // 2 - 40
    pygame.draw.rect(screen, RESISTOR_COLOR, (resistor_x, resistor_y, 160, 80))
    
    # Обновление и отрисовка частиц в проводе
    for particle in wire_particles:
        particle.update(voltage_slider.value)
        particle.draw(voltage_slider.value)
    
    # Обновление и отрисовка частиц в резисторе
    for particle in resistor_particles:
        particle.update(voltage_slider.value * 10)
        particle.draw()
    
    # Отрисовка батарейки ПОВЕРХ провода
    pygame.draw.rect(screen, BATTERY_COLOR, (battery_x, battery_y, battery_width, battery_height))
    pygame.draw.rect(screen, (0, 0, 0), (battery_x + 5, battery_y + 5, battery_width - 10, battery_height - 10))
    
    # Определение цветов полюсов в зависимости от напряжения
    if voltage_slider.value > 0:
        plus_color = (0, 255, 0)  # Зеленый для положительного
        minus_color = (255, 0, 0)  # Красный для отрицательного
        # При положительном напряжении: плюс справа, минус слева
        plus_pos = (battery_x + battery_width - 40, battery_y + 15)
        minus_pos = (battery_x + 20, battery_y + 15)
    elif voltage_slider.value < 0:
        plus_color = (255, 0, 0)  # Красный когда напряжение отрицательное
        minus_color = (0, 255, 0)  # Зеленый когда напряжение отрицательное
        # При отрицательном напряжении: плюс слева, минус справа
        plus_pos = (battery_x + 20, battery_y + 15)
        minus_pos = (battery_x + battery_width - 40, battery_y + 15)
    else:
        plus_color = (200, 200, 200)  # Серый при нулевом напряжении
        minus_color = (200, 200, 200)  # Серый при нулевом напряжении
        plus_pos = (battery_x + 20, battery_y + 15)
        minus_pos = (battery_x + battery_width - 40, battery_y + 15)
    
    # Отрисовка полюсов батарейки
    plus_text = font_large.render("+", True, plus_color)
    minus_text = font_large.render("-", True, minus_color)
    screen.blit(plus_text, plus_pos)
    screen.blit(minus_text, minus_pos)
    
    # Отрисовка трекбара
    voltage_slider.draw()
    
    # Отображение температуры
    temperature = abs(voltage_slider.value) * 8 + 20  # Температура зависит от скорости
    temp_text = font.render(f"Температура резистора: {temperature:.1f} °C", True, TEXT_COLOR)
    screen.blit(temp_text, (WIDTH // 2 - 120, HEIGHT - 100))
    
    # Отображение направления тока
    direction = "←" if voltage_slider.value > 0 else "→" if voltage_slider.value < 0 else "○"
    direction_text = font.render(f"Направление тока: {direction} (от + к -)", True, TEXT_COLOR)
    screen.blit(direction_text, (WIDTH // 2 - 100, HEIGHT - 130))
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
