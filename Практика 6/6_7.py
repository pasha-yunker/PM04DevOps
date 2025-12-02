# Импорт необходимых библиотек
import tkinter as tk  # для создания графического интерфейса
from tkinter import ttk  # для стилизованных виджетов
import numpy as np  # для математических операций и работы с массивами
import matplotlib.pyplot as plt  # для построения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # для встраивания графика в tkinter

# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Гармонические колебания | Работа Павла Юнкер")
# Устанавливаем размер окна
root.geometry("800x600")

# Создаем функцию для построения графика
def plot_harmonic():
    """
    Функция для построения графика гармонического колебания
    на основе текущих значений амплитуды и частоты
    """
    
    # Очищаем предыдущий график (если он был)
    ax.clear()
    
    # Получаем текущие значения амплитуды и частоты из полей ввода
    # Метод get() возвращает строку, поэтому преобразуем в float
    amplitude = float(amp_entry.get())
    frequency = float(freq_entry.get())
    
    # Создаем массив значений времени от 0 до 4π с шагом 0.01
    # Это даст нам достаточно точек для плавного графика
    t = np.arange(0, 4*np.pi, 0.01)
    
    # Вычисляем значения гармонического колебания по формуле:
    # y = A * sin(ωt), где ω = 2πf
    y = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Строим график: синяя линия толщиной 2 пикселя
    ax.plot(t, y, 'b-', linewidth=2)
    
    # Добавляем заголовок графика с текущими параметрами
    ax.set_title(f'Гармоническое колебание: A={amplitude}, f={frequency} Гц')
    
    # Добавляем подписи осей
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('Амплитуда')
    
    # Добавляем сетку для удобства чтения графика
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Автоматически подбираем масштаб осей для наилучшего отображения
    ax.autoscale_view()
    
    # Обновляем холст с графиком
    canvas.draw()

# Создаем функцию для сброса параметров к значениям по умолчанию
def reset_parameters():
    """
    Функция для сброса амплитуды и частоты к значениям по умолчанию
    """
    # Устанавливаем значения по умолчанию в поля ввода
    amp_entry.delete(0, tk.END)  # очищаем поле
    amp_entry.insert(0, "1.0")   # вставляем значение по умолчанию
    
    freq_entry.delete(0, tk.END)  # очищаем поле
    freq_entry.insert(0, "1.0")   # вставляем значение по умолчанию
    
    # Перестраиваем график с новыми параметрами
    plot_harmonic()

# Создаем область для элементов управления (фрейм)
control_frame = tk.Frame(root)
# Размещаем фрейм в верхней части окна с отступами
control_frame.pack(pady=10)

# Создаем метку и поле ввода для амплитуды
# Метка - текстовая подпись для поля ввода
amp_label = tk.Label(control_frame, text="Амплитуда (A):")
# Размещаем метку в сетке (первая строка, первый столбец)
amp_label.grid(row=0, column=0, padx=5, pady=5)

# Поле ввода для амплитуды
amp_entry = tk.Entry(control_frame, width=10)
# Вставляем значение по умолчанию
amp_entry.insert(0, "1.0")
# Размещаем поле ввода в сетке (первая строка, второй столбец)
amp_entry.grid(row=0, column=1, padx=5, pady=5)

# Создаем метку и поле ввода для частоты
freq_label = tk.Label(control_frame, text="Частота (f, Гц):")
# Размещаем метку в сетке (вторая строка, первый столбец)
freq_label.grid(row=1, column=0, padx=5, pady=5)

# Поле ввода для частоты
freq_entry = tk.Entry(control_frame, width=10)
# Вставляем значение по умолчанию
freq_entry.insert(0, "1.0")
# Размещаем поле ввода в сетке (вторая строка, второй столбец)
freq_entry.grid(row=1, column=1, padx=5, pady=5)

# Создаем кнопку для построения графика
plot_button = tk.Button(control_frame, text="Построить график", 
                       command=plot_harmonic,  # при нажатии вызываем функцию plot_harmonic
                       bg="lightblue",         # цвет фона
                       width=15)               # ширина кнопки
# Размещаем кнопку в сетке (первая строка, третий столбец)
plot_button.grid(row=0, column=2, padx=10, pady=5)

# Создаем кнопку для сброса параметров
reset_button = tk.Button(control_frame, text="Сбросить", 
                        command=reset_parameters,  # при нажатии вызываем функцию reset_parameters
                        bg="lightcoral",          # цвет фона
                        width=15)                 # ширина кнопки
# Размещаем кнопку в сетке (вторая строка, третий столбец)
reset_button.grid(row=1, column=2, padx=10, pady=5)

# Создаем фигуру matplotlib для графика
# figsize - размер фигуры в дюймах, dpi - разрешение
fig = plt.Figure(figsize=(8, 5), dpi=100)
# Добавляем субplot (область для построения графика) на фигуру
ax = fig.add_subplot(111)

# Создаем холст для встраивания графика в tkinter
# master - родительский виджет (главное окно), figure - фигура matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
# Получаем виджет холста
canvas_widget = canvas.get_tk_widget()
# Размещаем холст в окне с отступами
canvas_widget.pack(pady=10)

# Строим начальный график с параметрами по умолчанию
plot_harmonic()

# Запускаем главный цикл обработки событий tkinter
# Программа будет работать до закрытия окна
root.mainloop()