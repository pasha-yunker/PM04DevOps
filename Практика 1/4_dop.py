import tkinter as tk
from tkinter import ttk

def update_circle(event=None):
    # Получаем значение из TrackBar
    radius = trackbar.get()
    
    # Очищаем canvas
    canvas.delete("all")
    
    # Рисуем круг
    x, y = 300, 200
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                      fill="red", outline="black")
    
    # Обновляем текст
    label.config(text=f"Радиус: {radius}px")

# Создаем главное окно
root = tk.Tk()
root.title("Круг с изменяемым радиусом")
root.geometry("600x600")

# Создаем TrackBar (Scale)
trackbar = ttk.Scale(root, from_=10, to=200, orient="horizontal", command=update_circle)
trackbar.set(100)  # Начальное значение
trackbar.pack(pady=20)

# Создаем Label для отображения радиуса
label = tk.Label(root, text="Радиус: 100px", font=("Arial", 14))
label.pack()

# Создаем Canvas для рисования
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Инициализируем круг
update_circle()

# Запускаем приложение
root.mainloop()
