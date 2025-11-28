import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math
import os

class TextFileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор текстовых файлов | Работа Павла Юнкер")
        self.root.geometry("600x500")
        
        # Основные переменные
        self.filename = tk.StringVar(value="output.txt")
        self.custom_text = tk.StringVar(value="Произвольный текст для записи в файл")
        self.numbers_count = tk.IntVar(value=10)
        self.function_choice = tk.StringVar(value="sin")
        self.array_size = tk.IntVar(value=5)
        self.start_value = tk.DoubleVar(value=0)
        self.end_value = tk.DoubleVar(value=2 * math.pi)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для имени файла
        file_frame = ttk.LabelFrame(self.root, text="Настройки файла", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(file_frame, text="Имя файла:").grid(row=0, column=0, sticky="w")
        ttk.Entry(file_frame, textvariable=self.filename, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Обзор...", command=self.browse_file).grid(row=0, column=2, padx=5)
        
        # Фрейм для произвольного текста
        text_frame = ttk.LabelFrame(self.root, text="Произвольный текст", padding=10)
        text_frame.pack(fill="x", padx=10, pady=5)
        
        text_entry = tk.Text(text_frame, height=3, width=70)
        text_entry.pack(fill="x")
        text_entry.insert("1.0", self.custom_text.get())
        text_entry.bind("<KeyRelease>", lambda e: self.custom_text.set(text_entry.get("1.0", "end-1c")))
        
        # Фрейм для случайных чисел
        numbers_frame = ttk.LabelFrame(self.root, text="Случайные числа", padding=10)
        numbers_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(numbers_frame, text="Количество чисел:").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(numbers_frame, from_=1, to=1000, textvariable=self.numbers_count, width=10).grid(row=0, column=1, padx=5)
        
        # Фрейм для математической функции
        function_frame = ttk.LabelFrame(self.root, text="Математическая функция", padding=10)
        function_frame.pack(fill="x", padx=10, pady=5)
        
        # Выбор функции
        ttk.Label(function_frame, text="Функция:").grid(row=0, column=0, sticky="w", pady=(0, 6))
        function_combo = ttk.Combobox(function_frame, textvariable=self.function_choice, 
                                    values=["sin", "cos", "tan", "exp", "log"], state="readonly")
        function_combo.grid(row=0, column=1, padx=5, sticky="w", pady=(0, 6))
        
        # Размер массива
        ttk.Label(function_frame, text="Размер массива:").grid(row=1, column=0, sticky="w", pady=(0, 6))
        ttk.Spinbox(function_frame, from_=1, to=100, textvariable=self.array_size, width=10).grid(row=1, column=1, padx=5)
        
        # Диапазон значений
        ttk.Label(function_frame, text="Начальное значение:").grid(row=2, column=0, sticky="w", pady=(0, 6))
        ttk.Entry(function_frame, textvariable=self.start_value, width=15).grid(row=2, column=1, padx=5)
        
        ttk.Label(function_frame, text="Конечное значение:").grid(row=3, column=0, sticky="w", pady=(0, 6))
        ttk.Entry(function_frame, textvariable=self.end_value, width=15).grid(row=3, column=1, padx=5)
        
        # Кнопка генерации
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=20)
        
        ttk.Button(button_frame, text="Сгенерировать файл", command=self.generate_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить поля", command=self.clear_fields).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Просмотреть файл", command=self.view_file).pack(side="left", padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
    
    def browse_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.filename.set(filename)
    
    def generate_file(self):
        try:
            filename = self.filename.get()
            if not filename:
                messagebox.showerror("Ошибка", "Введите имя файла")
                return
            
            # Создаем содержимое файла
            content = self.generate_content()
            
            # Записываем в файл
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.status_var.set(f"Файл успешно создан: {filename}")
            messagebox.showinfo("Успех", f"Файл {filename} успешно создан!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.status_var.set("Ошибка при создании файла")
    
    def generate_content(self):
        content = []
        
        # 1. Произвольный текст
        content.append("=== ПРОИЗВОЛЬНЫЙ ТЕКСТ ===")
        content.append(self.custom_text.get())
        content.append("")
        
        # 2. Случайные числа
        content.append("=== СЛУЧАЙНЫЕ ЧИСЛА ===")
        numbers_count = self.numbers_count.get()
        random_numbers = [random.uniform(0, 100) for _ in range(numbers_count)]
        for i, num in enumerate(random_numbers, 1):
            content.append(f"{i:2d}. {num:.2f}")
        content.append("")
        
        # 3. Массив значений математической функции
        content.append("=== МАССИВ ЗНАЧЕНИЙ МАТЕМАТИЧЕСКОЙ ФУНКЦИИ ===")
        array_size = self.array_size.get()
        start = self.start_value.get()
        end = self.end_value.get()
        function_name = self.function_choice.get()
        
        # Выбираем функцию
        math_function = self.get_math_function(function_name)
        
        # Генерируем значения
        step = (end - start) / (array_size - 1) if array_size > 1 else 0
        function_values = []
        
        for i in range(array_size):
            x = start + i * step
            try:
                y = math_function(x)
                function_values.append((x, y))
            except (ValueError, ZeroDivisionError):
                function_values.append((x, float('nan')))
        
        # Записываем значения
        content.append(f"Функция: {function_name}")
        content.append(f"Диапазон: от {start} до {end}")
        content.append("")
        
        for i, (x, y) in enumerate(function_values, 1):
            if math.isnan(y):
                content.append(f"{i:2d}. x = {x:.2f}, y = не определено")
            else:
                content.append(f"{i:2d}. x = {x:.2f}, y = {y:.2f}")
        
        return "\n".join(content)
    
    def get_math_function(self, function_name):
        """Возвращает соответствующую математическую функцию"""
        functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'log': math.log
        }
        return functions.get(function_name, math.sin)
    
    def clear_fields(self):
        self.custom_text.set("")
        self.numbers_count.set(10)
        self.array_size.set(5)
        self.start_value.set(0)
        self.end_value.set(2 * math.pi)
        self.status_var.set("Поля очищены")
    
    def view_file(self):
        filename = self.filename.get()
        if not filename or not os.path.exists(filename):
            messagebox.showwarning("Предупреждение", "Файл не существует")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Создаем окно для просмотра
            view_window = tk.Toplevel(self.root)
            view_window.title(f"Просмотр файла: {filename}")
            view_window.geometry("700x500")
            
            # Текстовое поле с прокруткой
            text_frame = ttk.Frame(view_window)
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap="word")
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            text_widget.insert("1.0", content)
            text_widget.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")

def main():
    root = tk.Tk()
    app = TextFileGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()