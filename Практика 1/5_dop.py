import tkinter as tk
from tkinter import ttk
import math

class EllipseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Эллипс с эксцентриситетом")
        self.root.geometry("700x500")
        
        # Константы
        self.center_x, self.center_y = 300, 200
        self.a = 150  # большая полуось (фиксированная)
        
        # Переменные
        self.eccentricity = tk.DoubleVar(value=0.0)
        
        self.create_widgets()
        self.draw_ellipse()
    
    def create_widgets(self):
        # TrackBar для эксцентриситета
        ttk.Label(self.root, text="Эксцентриситет (0-0.9):", font=("Arial", 12)).pack(pady=10)
        
        self.trackbar = ttk.Scale(self.root, from_=0.0, to=0.9, 
                                orient="horizontal", 
                                variable=self.eccentricity,
                                command=self.on_trackbar_change)
        self.trackbar.pack(pady=5, padx=20, fill="x")
        
        # Label с значением
        self.value_label = ttk.Label(self.root, text="Эксцентриситет: 0.0", font=("Arial", 10))
        self.value_label.pack()
        
        # Canvas для рисования
        self.canvas = tk.Canvas(self.root, width=600, height=350, bg="white", relief="sunken", bd=2)
        self.canvas.pack(pady=20)
        
        # Кнопка сброса
        ttk.Button(self.root, text="Сброс", command=self.reset).pack(pady=5)
    
    def on_trackbar_change(self, event=None):
        e = self.eccentricity.get()
        self.value_label.config(text=f"Эксцентриситет: {e:.2f}")
        self.draw_ellipse()
    
    def draw_ellipse(self):
        self.canvas.delete("all")
        e = self.eccentricity.get()
        
        # Вычисляем малую полуось через эксцентриситет: e = sqrt(1 - (b²/a²))
        b = self.a * math.sqrt(1 - e**2)  # малая полуось
        
        # Рисуем эллипс
        self.canvas.create_oval(self.center_x - self.a, self.center_y - b,
                               self.center_x + self.a, self.center_y + b,
                               fill="lightblue", outline="darkblue", width=2)
        
        # Рисуем оси
        self.canvas.create_line(self.center_x - self.a - 10, self.center_y,
                               self.center_x + self.a + 10, self.center_y,
                               fill="red", width=1, arrow=tk.BOTH)
        self.canvas.create_line(self.center_x, self.center_y - b - 10,
                               self.center_x, self.center_y + b + 10,
                               fill="red", width=1, arrow=tk.BOTH)
        
        # Подписи осей
        self.canvas.create_text(self.center_x + self.a + 20, self.center_y, text="a", font=("Arial", 12))
        self.canvas.create_text(self.center_x, self.center_y - b - 20, text="b", font=("Arial", 12))
        
        # Фокусы эллипса
        c = e * self.a  # фокальное расстояние
        self.canvas.create_oval(self.center_x - c - 3, self.center_y - 3,
                               self.center_x - c + 3, self.center_y + 3,
                               fill="red")
        self.canvas.create_oval(self.center_x + c - 3, self.center_y - 3,
                               self.center_x + c + 3, self.center_y + 3,
                               fill="red")
    
    def reset(self):
        self.eccentricity.set(0.0)
        self.on_trackbar_change()

if __name__ == "__main__":
    root = tk.Tk()
    app = EllipseApp(root)
    root.mainloop()