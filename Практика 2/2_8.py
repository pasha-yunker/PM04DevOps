import tkinter as tk
from tkinter import messagebox
import random

def generate_numbers():
    try:
        # Получаем значения из полей ввода
        count = int(entry_count.get())
        min_val = int(entry_min.get())
        max_val = int(entry_max.get())
        
        # Проверяем допустимость значений
        if count <= 0 or count > 1000:
            messagebox.showerror("Ошибка", "Количество чисел должно быть от 1 до 1000")
            return
        
        if min_val >= max_val:
            messagebox.showerror("Ошибка", "Минимальное значение должно быть меньше максимального")
            return
        
        # Генерируем случайные числа
        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        
        # Очищаем текстовое поле и выводим результат
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, f"Сгенерировано {count} чисел от {min_val} до {max_val}:\n\n")
        
        # Выводим числа с переносами
        for i, num in enumerate(numbers):
            text_result.insert(tk.END, f"{num:6}")
            if (i + 1) % 10 == 0:  # 10 чисел в строке
                text_result.insert(tk.END, "\n")
        
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа")

# Создаем главное окно
root = tk.Tk()
root.title("Генератор случайных чисел | Работа Павла Юнкер")
root.geometry("600x500")

# Заголовок
label_title = tk.Label(root, text="Генератор случайных чисел", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# Фрейм для ввода параметров
frame_input = tk.Frame(root)
frame_input.pack(pady=10, padx=20, fill=tk.X)

# Количество чисел
label_count = tk.Label(frame_input, text="Количество чисел (до 1000):")
label_count.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_count = tk.Entry(frame_input, width=10)
entry_count.grid(row=0, column=1, padx=5, pady=5)
entry_count.insert(0, "10")

# Минимальное значение
label_min = tk.Label(frame_input, text="Минимальное значение:")
label_min.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_min = tk.Entry(frame_input, width=10)
entry_min.grid(row=1, column=1, padx=5, pady=5)
entry_min.insert(0, "1")

# Максимальное значение
label_max = tk.Label(frame_input, text="Максимальное значение:")
label_max.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_max = tk.Entry(frame_input, width=10)
entry_max.grid(row=2, column=1, padx=5, pady=5)
entry_max.insert(0, "100")

# Кнопка генерации
button_generate = tk.Button(root, text="Сгенерировать числа", command=generate_numbers, 
                           bg="lightblue", font=("Arial", 12))
button_generate.pack(pady=10)

# Текстовое поле для вывода результатов
text_result = tk.Text(root, height=15, width=70, wrap=tk.WORD)
text_result.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Добавляем скроллбар для текстового поля
scrollbar = tk.Scrollbar(text_result)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_result.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_result.yview)

# Запускаем главный цикл
root.mainloop()