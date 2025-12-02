import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Явно указываем бэкенд для matplotlib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def parse_bits(s: str):
    """Парсит строку с битами и возвращает список целых чисел"""
    s = s.strip().replace(" ", "")
    if not s:
        return None
    if any(ch not in '01' for ch in s):
        return None
    bits = [int(ch) for ch in s if ch in '01']
    return bits

def nrz(bits, sp=20):
    """NRZ кодирование: 0 -> 0, 1 -> 1"""
    level = np.array(bits, dtype=float)
    return np.repeat(level, sp)

def manchester(bits, sp=20):
    """Manchester кодирование: 0 -> 0->1, 1 -> 1->0"""
    half = max(1, sp // 2)
    seq = []
    for b in bits:
        if b == 0:
            seq.extend([0]*half + [1]*half)
        else:
            seq.extend([1]*half + [0]*half)
    return np.array(seq, dtype=float)

def mlt3(bits, sp=20):
    """MLT-3 кодирование: трехуровневое кодирование с циклическим изменением"""
    state = 0
    seq = []
    for b in bits:
        if b == 1:
            # переключаем состояние циклически
            if state == 0:
                state = 1
            elif state == 1:
                state = -1
            elif state == -1:
                state = 0
        # если 0, держим текущее состояние
        seq.extend([state]*sp)
    return np.array(seq, dtype=float)

def ami(bits, sp=20):
    """AMI кодирование: 0 -> 0, 1 -> чередование +1 и -1"""
    level = 1
    seq = []
    for b in bits:
        if b == 0:
            seq.extend([0]*sp)
        else:
            seq.extend([level]*sp)
            level *= -1
    return np.array(seq, dtype=float)

def impulsive(bits, sp=20):
    """Импульсное кодирование: 1 -> высокий импульс, 0 -> нулевой"""
    return np.repeat(np.array([1 if b==1 else 0 for b in bits], dtype=float), sp)

def plot_all(bits, sp=20, title="Кодирование сигнала"):
    """Строит графики всех типов кодирования"""
    t = np.arange(len(bits)*sp)
    y_nrz = nrz(bits, sp)
    y_man = manchester(bits, sp)
    y_mlt3 = mlt3(bits, sp)
    y_ami = ami(bits, sp)
    y_imp = impulsive(bits, sp)

    # Создаем фигуру с 5 подграфиками
    fig = plt.figure(figsize=(12, 10))
    
    # Устанавливаем общий заголовок для всего окна
    fig.canvas.manager.set_window_title(title)
    
    plots_data = [
        (y_nrz, 'blue', 'NRZ (Non-Return to Zero)'),
        (y_man, 'red', 'Manchester'),
        (y_mlt3, 'green', 'MLT-3 (Multi-Level Transmission)'),
        (y_ami, 'purple', 'AMI (Alternate Mark Inversion)'),
        (y_imp, 'orange', 'Impulsive (Импульсное)')
    ]
    
    for i, (y_data, color, plot_title) in enumerate(plots_data):
        ax = plt.subplot(5, 1, i+1)
        ax.plot(t, y_data, drawstyle='steps-post', color=color, linewidth=2)
        ax.set_title(plot_title, pad=10)
        ax.set_ylabel('Уровень')
        ax.grid(True, alpha=0.3)
        if i == 4:
            ax.set_xlabel('Время (отсчеты)')

    # Увеличиваем расстояние между подграфиками
    plt.tight_layout(pad=3.0, h_pad=1.5)
    
    # Обновляем отображение
    plt.draw()
    plt.show(block=False)  # block=False позволяет не блокировать основной поток

def on_plot():
    """Обработчик нажатия кнопки для построения графиков"""
    s = text.get("1.0", tk.END).strip()
    bits = parse_bits(s)
    
    if bits is None:
        messagebox.showerror("Ошибка", 
            "Введите корректную битовую последовательность!\n"
            "Допускаются только символы 0 и 1.\n"
            "Пример: 1011001 или 1 0 1 1 0 0 1")
        return
    
    if len(bits) == 0:
        messagebox.showwarning("Предупреждение", "Введите хотя бы один бит!")
        return
    
    # Обновляем информацию о введенной последовательности
    info_label.config(text=f"Введено битов: {len(bits)} | Последовательность: {''.join(map(str, bits))}")
    
    # Показываем сообщение о построении графиков
    status_label.config(text="Построение графиков...", foreground="blue")
    root.update()
    
    try:
        plot_all(bits, sp=20, title=f"Кодирование: {''.join(str(b) for b in bits)}")
        status_label.config(text="Графики успешно построены!", foreground="green")
    except Exception as e:
        status_label.config(text="Ошибка при построении графиков!", foreground="red")
        messagebox.showerror("Ошибка", f"Не удалось построить графики:\n{str(e)}")

def clear_text():
    """Очищает текстовое поле"""
    text.delete("1.0", tk.END)
    info_label.config(text="Введено битов: 0")
    status_label.config(text="Готов к работе")

def insert_example():
    """Вставляет пример битовой последовательности"""
    text.delete("1.0", tk.END)
    text.insert("1.0", "1011001")
    info_label.config(text="Вставлен пример: 1011001")

# Создаем главное окно
root = tk.Tk()
root.title("Визуализатор методов кодирования сигналов")
root.geometry("700x550")

# Создаем основной фрейм
main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

# Заголовок
title_label = ttk.Label(main_frame, 
                       text="Визуализатор методов кодирования цифровых сигналов",
                       font=("Arial", 14, "bold"),
                       foreground="darkblue")
title_label.pack(pady=(0, 15))

# Описание
desc_label = ttk.Label(main_frame,
                      text="Введите битовую последовательность для визуализации различных методов кодирования",
                      font=("Arial", 10),
                      wraplength=500)
desc_label.pack(pady=(0, 10))

# Метка для поля ввода
input_label = ttk.Label(main_frame, text="Битовая последовательность (только 0 и 1):")
input_label.pack(anchor="w", pady=(0, 5))

# Текстовое поле для ввода
text_frame = ttk.Frame(main_frame)
text_frame.pack(fill=tk.X, pady=(0, 10))

text = tk.Text(text_frame, width=50, height=4, font=("Courier New", 10))
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scrollbar.set)

# Фрейм для кнопок
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=10)

# Кнопка для вставки примера
example_btn = ttk.Button(button_frame, text="Вставить пример", command=insert_example)
example_btn.pack(side=tk.LEFT, padx=(0, 10))

# Кнопка очистки
clear_btn = ttk.Button(button_frame, text="Очистить", command=clear_text)
clear_btn.pack(side=tk.LEFT, padx=(0, 10))

# Кнопка построения графиков
plot_btn = ttk.Button(button_frame, text="Построить графики", command=on_plot)
plot_btn.pack(side=tk.LEFT)

# Информационная метка
info_label = ttk.Label(main_frame, text="Введено битов: 0", font=("Arial", 9))
info_label.pack(anchor="w", pady=(10, 5))

# Статусная метка
status_label = ttk.Label(main_frame, text="Готов к работе", font=("Arial", 9))
status_label.pack(anchor="w", pady=(0, 10))

# Фрейм с информацией о методах кодирования
methods_frame = ttk.LabelFrame(main_frame, text="Методы кодирования", padding="10")
methods_frame.pack(fill=tk.X, pady=10)

methods_text = """
• NRZ (Non-Return to Zero) - 0=низкий уровень, 1=высокий уровень
• Manchester - 0=переход низкий→высокий, 1=переход высокий→низкий  
• MLT-3 (Multi-Level Transmission) - трехуровневое кодирование с циклическим изменением
• AMI (Alternate Mark Inversion) - 0=0, 1=чередование +1 и -1
• Impulsive - 1=импульс, 0=отсутствие сигнала
"""

methods_desc = tk.Text(methods_frame, width=60, height=6, font=("Arial", 9), wrap=tk.WORD)
methods_desc.pack(fill=tk.BOTH)
methods_desc.insert("1.0", methods_text)
methods_desc.config(state=tk.DISABLED)  # Делаем текст только для чтения

# Запускаем главный цикл
root.mainloop()