import tkinter as tk
import math
from tkinter import ttk

class SpeedometerWidget(tk.Canvas):
    def __init__(self, parent, width=500, height=400):
        super().__init__(parent, width=width, height=height, bg='white')
        self.width = width
        self.height = height
        self.value = 0  # Текущее значение прогресса (0-100)
        
    def set_value(self, value):
        """Установка значения прогресса с ограничением в диапазоне 0-100"""
        self.value = max(0, min(100, int(value)))  # Ограничиваем значение между 0 и 100, преобразуем в целое
        self.draw_speedometer()  # Перерисовываем виджет
        
    def draw_speedometer(self):
        """Метод отрисовки спидометра"""
        self.delete("all")  # Очищаем холст
        
        # Размеры и позиционирование
        width = self.width
        height = self.height
        
        # Определяем размеры спидометра
        diameter = min(width, height) - 80  # Диаметр спидометра
        center_x = width // 2  # Центр по X
        center_y = height - 100  # Центр по Y (смещен вниз для дуги)
        radius = diameter // 2  # Радиус спидометра
        
        # Рисуем основную дугу спидометра (фон)
        self.draw_background_arc(center_x, center_y, radius)
        
        # Рисуем прогресс-бар (голубая дуга) с кружком на конце
        self.draw_progress_arc(center_x, center_y, radius)
        
        # Рисуем деления и метки по дуге (как на спидометре)
        self.draw_scale(center_x, center_y + 6, radius + 5)
        
        # Отображаем текущее значение
        self.draw_value(center_x, center_y)
        
    def draw_background_arc(self, center_x, center_y, radius):
        """Рисуем фон спидометра (серая дуга)"""
        # Координаты ограничивающего прямоугольника для дуги
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        
        # Рисуем дугу от 180 до 0 градусов (полукруг сверху)
        # В tkinter углы задаются в градусах, начало в 3 часа, положительное направление - против часовой
        start_angle = 180  # Начальный угол 180° (слева)
        extent = 180  # Длина дуги 180° (идем против часовой стрелки вправо)
        
        # Рисуем дугу (светло-серая, толщина 16)
        """self.create_arc(x1, y1, x2, y2, 
                       start=start_angle, extent=extent,
                       outline='#C8C8C8', width=16, style=tk.ARC)"""
        
    def draw_progress_arc(self, center_x, center_y, radius):
        """Рисуем голубой прогресс-бар поверх фона с кружком на конце"""
        progress_color = '#64C8FF'  # Голубой цвет
        
        # Координаты ограничивающего прямоугольника для дуги
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        
        # Угол прогресса: от 0 до 180 градусов в зависимости от значения
        progress_angle = -(180 * (self.value / 100)) # Процент от полной дуги
        
        # Рисуем дугу прогресса (идем слева направо против часовой стрелки)
        start_angle = 180  # Начинаем с 180 градусов (слева)
        extent = progress_angle  # Положительное значение для рисования против часовой стрелки
        
        self.create_arc(x1, y1, x2, y2, 
                       start=start_angle, extent=extent,
                       outline=progress_color, width=16, style=tk.ARC)
        
        # Рисуем кружок на конце дуги, если значение > 0
        if self.value >= 0:
            angle_deg = 180 - progress_angle # угол в градусах
            angle_rad = math.radians(angle_deg)
            
            # Координаты точки на окружности
            circle_radius = 10  # радиус кружка
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            
            self.create_oval(x - circle_radius, y - circle_radius,
                           x + circle_radius, y + circle_radius,
                           fill=progress_color, outline=progress_color)
        
    def draw_scale(self, center_x, center_y, radius):
        """Рисуем шкалу с делениями и метками по дуге прогресс-бара"""
        # Рисуем деления каждые 10% по дуге прогресс-бара
        for i in range(0, 101, 10):
            # Вычисляем угол для текущего деления (от 180 до 0 градусов)
            angle_degrees = -(180 - (180 * i / 100))  # От 180° (слева) до 0° (справа)
            angle = math.radians(angle_degrees)
            
            # Определяем параметры деления в зависимости от типа
            if i % 20 == 0:  # Длинные деления для 0, 20, 40, 60, 80, 100
                color = '#323232'
                line_width = 2
                inner_radius = radius - 25  # Внутренний радиус (ближе к центру)
                outer_radius = radius + 7   # Внешний радиус (наружу от прогресс-бара)
            else:  # Короткие деления для 10, 30, 50, 70, 90
                color = '#646464'
                line_width = 1
                inner_radius = radius - 20  # Внутренний радиус
                outer_radius = radius + 8   # Внешний радиус
            
            # Координаты начала и конца деления
            x1 = center_x + inner_radius * math.cos(angle)
            y1 = center_y + inner_radius * math.sin(angle)
            x2 = center_x + outer_radius * math.cos(angle)
            y2 = center_y + outer_radius * math.sin(angle)
            
            self.create_line(x1, y1, x2, y2, fill=color, width=line_width)
            
            # Добавляем текст метки для всех делений с шагом 10
            text_radius = radius + 35  # Радиус для размещения текста (еще дальше наружу)
            text_x = center_x + text_radius * math.cos(angle)
            text_y = center_y + text_radius * math.sin(angle)
            
            text = f"{i}"
            
            # Центрируем текст относительно деления
            self.create_text(text_x, text_y, text=text, font=('Arial', 10))
        
        # Дополнительно рисуем маленькие деления каждые 5%
        for i in range(0, 101, 5):
            if i % 10 != 0:  # Пропускаем основные деления
                angle_degrees = -((180 * i / 100))
                angle = math.radians(angle_degrees)
                
                color = '#646464'
                inner_radius = radius - 18  # Внутренний радиус
                outer_radius = radius + 5   # Внешний радиус
                
                x1 = center_x + inner_radius * math.cos(angle)
                y1 = center_y + inner_radius * math.sin(angle)
                x2 = center_x + outer_radius * math.cos(angle)
                y2 = center_y + outer_radius * math.sin(angle)
                
                self.create_line(x1, y1, x2, y2, fill=color, width=1)
                
    def draw_value(self, center_x, center_y):
        """Отображаем текущее значение в центре спидометра"""
        # Отображаем значение в процентах (целое число)
        value_text = f"{int(self.value)}%"
        
        # Большой текст со значением
        self.create_text(center_x, center_y, text=value_text, 
                        font=('Arial', 24, 'bold'), fill='#0050A0')
        
        # Добавляем подпись под значением
        label_text = "Текущий прогресс"
        self.create_text(center_x, center_y + 40, text=label_text, 
                        font=('Arial', 12), fill='#0050A0')

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Спидометр с прогресс-баром | Работа Павла Юнкер')
        self.root.geometry('600x500')
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создаем основной фрейм
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем спидометр
        self.speedometer = SpeedometerWidget(main_frame, width=500, height=400)
        self.speedometer.pack(pady=10)
        
        # Создаем слайдер для управления значением
        self.slider = ttk.Scale(main_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                               command=self.on_slider_change)
        self.slider.set(45)  # Начальное значение
        self.slider.pack(fill=tk.X, padx=20, pady=10)
        
        # Добавляем метку для отображения текущего значения слайдера
        self.value_label = tk.Label(main_frame, text="Текущее значение: 45", 
                                   font=('Arial', 10))
        self.value_label.pack(pady=5)
        
        # Метка для описания
        label = tk.Label(main_frame, 
                        text="Используйте слайдер для изменения значения прогресса (0-100%)")
        label.pack(pady=5)
        
        # Первоначальная отрисовка спидометра
        self.speedometer.draw_speedometer()
        
    def on_slider_change(self, value):
        """Обработчик изменения значения слайдера"""
        int_value = int(float(value))  # Преобразуем в целое число
        self.speedometer.set_value(int_value)
        self.value_label.config(text=f"Текущее значение: {int_value}")
        
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

def main():
    app = MainWindow()
    app.run()

if __name__ == '__main__':
    main()