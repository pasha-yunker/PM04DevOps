import tkinter as tk
from tkinter import ttk

class CircularProgressBar:
    def __init__(self, parent, width=200, height=200):
        self.parent = parent
        self.width = width
        self.height = height
        self.value = 0
        self.max_value = 100
        
        # Создаем canvas для отрисовки прогресс-бара
        self.canvas = tk.Canvas(parent, width=width, height=height, bg='white')
        self.canvas.pack(pady=10)
        
        # Параметры окружности
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 2 - 10
        
        # Цвета
        self.bg_color = '#e0e0e0'
        self.progress_color = '#4CAF50'
        self.text_color = '#333333'
        
        # Отрисовываем начальное состояние
        self.draw()
    
    def draw(self):
        """Отрисовка прогресс-бара"""
        self.canvas.delete("all")
        
        # Фоновая окружность
        self.canvas.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            outline=self.bg_color,
            width=8,
            fill=''
        )
        
        # Прогресс (дуга)
        if self.value > 0:
            # При значении 100 рисуем полный круг
            if self.value == self.max_value:
                self.canvas.create_oval(
                    self.center_x - self.radius,
                    self.center_y - self.radius,
                    self.center_x + self.radius,
                    self.center_y + self.radius,
                    outline=self.progress_color,
                    width=8,
                    fill=''
                )
            else:
                angle = 360 * (self.value / self.max_value)
                self.canvas.create_arc(
                    self.center_x - self.radius,
                    self.center_y - self.radius,
                    self.center_x + self.radius,
                    self.center_y + self.radius,
                    start=90,
                    extent=-angle,
                    outline=self.progress_color,
                    width=8,
                    style=tk.ARC
                )
        
        # Текст с процентом (целое число)
        percent = int((self.value / self.max_value) * 100)
        self.canvas.create_text(
            self.center_x,
            self.center_y,
            text=f"{percent}%",
            font=('Arial', 16, 'bold'),
            fill=self.text_color
        )
        
    
    
    def set_value(self, value):
        """Установка значения прогресс-бара (целое число)"""
        self.value = max(0, min(int(value), self.max_value))
        self.draw()
    
    def get_value(self):
        """Получение текущего значения"""
        return self.value

def create_progress_bar_app():
    """Создание приложения с круглым прогресс-баром и трекбаром"""
    root = tk.Tk()
    root.title("Круглый прогресс-бар | Работа Павла Юнкер")
    root.geometry("300x350")
    
    # Создаем прогресс-бар
    progress_bar = CircularProgressBar(root, width=200, height=200)
    
    # Фрейм для элементов управления
    control_frame = tk.Frame(root)
    control_frame.pack(pady=20)
    
  
    
    # Трекбар (слайдер)
    scale = ttk.Scale(
        control_frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=200,
        command=lambda val: update_progress(val)
    )
    scale.set(0)
    scale.pack(pady=10)
    
    def update_progress(value):
        """Обновление прогресс-бара"""
        int_value = int(float(value))  # Преобразуем в целое число
        progress_bar.set_value(int_value)
        """value_label.config(text=f"{int_value}")"""
    
    root.mainloop()

if __name__ == "__main__":
    create_progress_bar_app()