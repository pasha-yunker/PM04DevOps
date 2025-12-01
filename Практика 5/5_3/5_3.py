import tkinter as tk
from math import cos, sin, pi
import time
from datetime import datetime

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Аналоговые часы | Работа Павла Юнкер")
        self.root.geometry("400x450")
        self.root.configure(bg='#1a1a1a')
        
        # Создаем canvas для рисования часов
        self.canvas = tk.Canvas(root, width=400, height=400, bg='#1a1a1a', 
                               highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Метка для цифрового времени
        self.digital_time = tk.Label(root, text="", font=('Arial', 14, 'bold'), 
                                   fg='#ffffff', bg='#1a1a1a')
        self.digital_time.pack()
        
        # Параметры часов
        self.center_x = 200
        self.center_y = 200
        self.radius = 150
        
        self.draw_clock_face()
        self.update_clock()
    
    def draw_clock_face(self):
        """Рисуем циферблат часов"""
        # Основной круг циферблата - цвет слоновой кости
        self.canvas.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill='#f8f4e9',
            outline='#8B4513',
            width=3
        )
        
        # Внутренний декоративный круг
        self.canvas.create_oval(
            self.center_x - self.radius + 10,
            self.center_y - self.radius + 10,
            self.center_x + self.radius - 10,
            self.center_y + self.radius - 10,
            outline='#d4c9b1',
            width=1
        )
        
        # Рисуем цифры и метки
        for i in range(1, 13):
            angle = pi/2 - 2*pi*i/12
            # УВЕЛИЧИВАЕМ отступ цифр от края - теперь 40 вместо 25
            number_radius = self.radius - 40
            
            # Позиция для цифр
            x = self.center_x + number_radius * cos(angle)
            y = self.center_y - number_radius * sin(angle)
            
            # Рисуем цифры в классическом стиле
            self.canvas.create_text(
                x, y,
                text=str(i),
                font=('Times New Roman', 18, 'bold'),
                fill='#2F4F4F'
            )
            
            # Рисуем крупные метки для часов (оставляем на прежнем месте)
            inner_radius = self.radius - 8
            outer_radius = self.radius - 18
            
            x1 = self.center_x + inner_radius * cos(angle)
            y1 = self.center_y - inner_radius * sin(angle)
            x2 = self.center_x + outer_radius * cos(angle)
            y2 = self.center_y - outer_radius * sin(angle)
            
            self.canvas.create_line(x1, y1, x2, y2, 
                                  fill='#8B4513', width=4)
        
        # Рисуем маленькие метки для минут
        for i in range(60):
            if i % 5 != 0:  # Пропускаем места где уже есть часовые метки
                angle = pi/2 - 2*pi*i/60
                inner_radius = self.radius - 8
                outer_radius = self.radius - 13
                
                x1 = self.center_x + inner_radius * cos(angle)
                y1 = self.center_y - inner_radius * sin(angle)
                x2 = self.center_x + outer_radius * cos(angle)
                y2 = self.center_y - outer_radius * sin(angle)
                
                self.canvas.create_line(x1, y1, x2, y2, 
                                      fill='#8B4513', width=2)
    
    def draw_tapered_hand(self, angle, length, start_width, end_width, color, tag):
        """Рисует сужающуюся стрелку"""
        # Основная линия стрелки
        x_end = self.center_x + length * cos(angle)
        y_end = self.center_y - length * sin(angle)
        
        # Перпендикулярный вектор для создания сужения
        perp_angle = angle + pi/2
        perp_x = cos(perp_angle)
        perp_y = -sin(perp_angle)  # Отрицательный из-за системы координат canvas
        
        # Точки для многоугольника стрелки
        x1 = self.center_x + (start_width/2) * perp_x
        y1 = self.center_y + (start_width/2) * perp_y
        x2 = self.center_x - (start_width/2) * perp_x
        y2 = self.center_y - (start_width/2) * perp_y
        x3 = x_end - (end_width/2) * perp_x
        y3 = y_end - (end_width/2) * perp_y
        x4 = x_end + (end_width/2) * perp_x
        y4 = y_end + (end_width/2) * perp_y
        
        # Рисуем стрелку как многоугольник
        self.canvas.create_polygon(
            x1, y1, x4, y4, x3, y3, x2, y2,
            fill=color, outline='#000000', width=1, tags=tag
        )
    
    def update_clock(self):
        """Обновляет положение стрелок"""
        # Удаляем предыдущие стрелки
        self.canvas.delete("hands")
        
        # Получаем текущее время
        now = datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second
        milliseconds = now.microsecond // 1000
        
        # Вычисляем углы для стрелок (в радианах)
        # Секундная стрелка с плавным движением
        second_angle = pi/2 - 2*pi*(seconds + milliseconds/1000)/60
        # Минутная стрелка с плавным движением
        minute_angle = pi/2 - 2*pi*(minutes + seconds/60)/60
        # Часовая стрелка с плавным движением
        hour_angle = pi/2 - 2*pi*(hours + minutes/60)/12
        
        # Рисуем стрелки с сужением:
        # Часовая стрелка - короткая и широкая, темно-синяя
        self.draw_tapered_hand(hour_angle, self.radius * 0.5, 12, 4, '#2F4F4F', "hands")
        
        # Минутная стрелка - средней длины, синяя
        self.draw_tapered_hand(minute_angle, self.radius * 0.7, 8, 2, '#4682B4', "hands")
        
        # Секундная стрелка - длинная и тонкая, красная
        self.draw_tapered_hand(second_angle, self.radius * 0.85, 4, 1, '#DC143C', "hands")
        
        # Центр часов - латунный цвет с ободком
        self.canvas.create_oval(
            self.center_x - 8, self.center_y - 8,
            self.center_x + 8, self.center_y + 8,
            fill='#B8860B', outline='#8B4513', width=2,
            tags="hands"
        )
        
        # Внутренний центр
        self.canvas.create_oval(
            self.center_x - 4, self.center_y - 4,
            self.center_x + 4, self.center_y + 4,
            fill='#FFD700', outline='',
            tags="hands"
        )
        
        # Обновляем цифровое время
        time_str = now.strftime("%H:%M:%S")
        self.digital_time.config(text=time_str)
        
        # Планируем следующее обновление через 50ms для плавной анимации
        self.root.after(50, self.update_clock)

def main():
    root = tk.Tk()
    clock = AnalogClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()