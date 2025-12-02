# Импорт необходимых библиотек
import tkinter as tk  # импортирует библиотеку tkinter для создания графического интерфейса
from tkinter import ttk  # импортирует модуль ttk для стилизованных виджетов
import numpy as np  # импортирует библиотеку numpy для математических операций с массивами
import matplotlib.pyplot as plt  # импортирует библиотеку matplotlib для построения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # импортирует класс для встраивания графиков в tkinter

# Создаем главное окно приложения
root = tk.Tk()  # создает главное окно приложения
root.title("Амплитудная модуляция | Работа Павла Юнкер")  # устанавливает заголовок окна
root.geometry("1000x800")  # устанавливает размер окна 1000x800 пикселей

# Глобальные переменные для параметров модуляции
carrier_freq = tk.DoubleVar(value=10.0)  # создает переменную для несущей частоты с начальным значением 10 Гц
carrier_amp = tk.DoubleVar(value=1.0)  # создает переменную для амплитуды несущей с начальным значением 1.0
modulation_freq = tk.DoubleVar(value=1.0)  # создает переменную для частоты модулирующего сигнала с начальным значением 1 Гц
modulation_depth = tk.DoubleVar(value=0.5)  # создает переменную для глубины модуляции с начальным значением 0.5 (50%)

# Функция для расчета амплитудной модуляции
def amplitude_modulation(t, fc, Ac, fm, m):
    """
    Функция для расчета амплитудно-модулированного сигнала
    Формула: AM(t) = Ac * [1 + m * cos(2πfm * t)] * cos(2πfc * t)
    где:
    t - время
    fc - несущая частота
    Ac - амплитуда несущей
    fm - частота модулирующего сигнала
    m - глубина модуляции (0 < m <= 1)
    """
    # Вычисляем модулирующий сигнал (низкочастотный)
    modulating_signal = Ac * (1 + m * np.cos(2 * np.pi * fm * t))  # вычисляет огибающую: Ac * [1 + m * cos(2πfm * t)]
    
    # Вычисляем несущий сигнал (высокочастотный)
    carrier_signal = np.cos(2 * np.pi * fc * t)  # вычисляет несущую: cos(2πfc * t)
    
    # Вычисляем амплитудно-модулированный сигнал
    am_signal = modulating_signal * carrier_signal  # перемножаем огибающую и несущую для получения AM сигнала
    
    return am_signal, modulating_signal, carrier_signal  # возвращаем AM сигнал, огибающую и несущую

# Функция для обновления графиков
def update_plots():
    """
    Функция для обновления всех графиков при изменении параметров
    """
    # Получаем текущие значения параметров из переменных
    fc = carrier_freq.get()  # получает текущее значение несущей частоты
    Ac = carrier_amp.get()  # получает текущее значение амплитуды несущей
    fm = modulation_freq.get()  # получает текущее значение частоты модуляции
    m = modulation_depth.get()  # получает текущее значение глубины модуляции
    
    # Создаем массив времени от 0 до 2 секунд с мелким шагом для плавности
    t = np.linspace(0, 2, 2000)  # создает 2000 точек времени от 0 до 2 секунд
    
    # Вычисляем сигналы
    am_signal, modulating_signal, carrier_signal = amplitude_modulation(t, fc, Ac, fm, m)  # вызывает функцию AM модуляции
    
    # Очищаем все графики
    for ax in [ax1, ax2, ax3, ax4]:  # цикл по всем областям графиков
        ax.clear()  # очищает каждую область графика
    
    # График 1: Модулирующий сигнал (низкочастотный)
    ax1.plot(t, modulating_signal, 'g-', linewidth=2, label='Модулирующий сигнал')  # строит график огибающей зеленым цветом
    ax1.set_title('Модулирующий сигнал (огибающая)')  # устанавливает заголовок для первого графика
    ax1.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax1.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax1.grid(True, alpha=0.3)  # добавляет сетку с прозрачностью 30%
    ax1.legend()  # добавляет легенду
    
    # График 2: Несущий сигнал
    ax2.plot(t, carrier_signal, 'r-', linewidth=1, alpha=0.7, label='Несущая')  # строит график несущей красным цветом
    ax2.set_title('Несущий сигнал')  # устанавливает заголовок для второго графика
    ax2.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax2.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax2.grid(True, alpha=0.3)  # добавляет сетку
    ax2.legend()  # добавляет легенду
    
    # График 3: Амплитудно-модулированный сигнал
    ax3.plot(t, am_signal, 'b-', linewidth=1.5, label='AM сигнал')  # строит график AM сигнала синим цветом
    # Также показываем огибающую
    ax3.plot(t, modulating_signal, 'g--', linewidth=1, alpha=0.7, label='Огибающая')  # добавляет пунктирную линию огибающей
    ax3.plot(t, -modulating_signal, 'g--', linewidth=1, alpha=0.7)  # добавляет нижнюю огибающую
    ax3.set_title('Амплитудно-модулированный сигнал')  # устанавливает заголовок для третьего графика
    ax3.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax3.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax3.grid(True, alpha=0.3)  # добавляет сетку
    ax3.legend()  # добавляет легенду
    
    # График 4: Все сигналы вместе для сравнения
    ax4.plot(t, modulating_signal, 'g-', linewidth=2, label='Модулирующий')  # строит модулирующий сигнал
    ax4.plot(t, carrier_signal, 'r-', linewidth=1, alpha=0.5, label='Несущая')  # строит несущую
    ax4.plot(t, am_signal, 'b-', linewidth=1.5, alpha=0.8, label='AM сигнал')  # строит AM сигнал
    ax4.set_title('Все сигналы')  # устанавливает заголовок для четвертого графика
    ax4.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax4.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax4.grid(True, alpha=0.3)  # добавляет сетку
    ax4.legend()  # добавляет легенду
    
    # Настраиваем внешний вид графиков
    for ax in [ax1, ax2, ax3, ax4]:  # цикл по всем графикам
        ax.set_xlim(0, 2)  # устанавливает одинаковые пределы по оси X для всех графиков
    
    # Автоматически подбираем масштаб по оси Y для каждого графика
    ax1.autoscale(axis='y')  # автоматически настраивает масштаб по Y для первого графика
    ax2.autoscale(axis='y')  # для второго графика
    ax3.autoscale(axis='y')  # для третьего графика
    ax4.autoscale(axis='y')  # для четвертого графика
    
    # Обновляем информацию о параметрах
    update_info_text(fc, Ac, fm, m)  # вызывает функцию обновления текстовой информации
    
    # Обновляем холст с графиками
    canvas.draw()  # перерисовывает холст чтобы отобразить все изменения

# Функция для обновления текстовой информации
def update_info_text(fc, Ac, fm, m):
    """
    Функция для обновления текстовой информации о параметрах модуляции
    """
    # Очищаем текстовое поле
    info_text.delete('1.0', tk.END)  # удаляет весь текст из текстового поля
    
    # Добавляем информацию о параметрах
    info_text.insert(tk.END, "Параметры амплитудной модуляции:\n")  # вставляет заголовок
    info_text.insert(tk.END, "=" * 40 + "\n\n")  # добавляет разделительную линию
    
    # Формула AM модуляции
    info_text.insert(tk.END, "Формула AM модуляции:\n")  # вставляет подзаголовок
    info_text.insert(tk.END, "AM(t) = Ac * [1 + m * cos(2πfm * t)] * cos(2πfc * t)\n\n")  # вставляет математическую формулу
    
    # Текущие параметры
    info_text.insert(tk.END, "Текущие параметры:\n")  # вставляет подзаголовок
    info_text.insert(tk.END, f"Несущая частота (fc): {fc:.1f} Гц\n")  # выводит несущую частоту
    info_text.insert(tk.END, f"Амплитуда несущей (Ac): {Ac:.1f}\n")  # выводит амплитуду несущей
    info_text.insert(tk.END, f"Частота модуляции (fm): {fm:.1f} Гц\n")  # выводит частоту модуляции
    info_text.insert(tk.END, f"Глубина модуляции (m): {m:.2f} ({m*100:.0f}%)\n\n")  # выводит глубину модуляции в долях и процентах
    
    # Дополнительная информация
    info_text.insert(tk.END, "Характеристики сигнала:\n")  # вставляет подзаголовок
    upper_sideband = fc + fm  # вычисляет верхнюю боковую полосу
    lower_sideband = fc - fm  # вычисляет нижнюю боковую полосу
    info_text.insert(tk.END, f"Верхняя боковая полоса: {upper_sideband:.1f} Гц\n")  # выводит верхнюю боковую полосу
    info_text.insert(tk.END, f"Нижняя боковая полоса: {lower_sideband:.1f} Гц\n")  # выводит нижнюю боковую полосу
    info_text.insert(tk.END, f"Ширина полосы: {2*fm:.1f} Гц\n")  # выводит ширину полосы (2*fm)

# Функция для сброса параметров к значениям по умолчанию
def reset_parameters():
    """
    Функция для сброса всех параметров к значениям по умолчанию
    """
    carrier_freq.set(10.0)  # устанавливает несущую частоту в 10 Гц
    carrier_amp.set(1.0)  # устанавливает амплитуду несущей в 1.0
    modulation_freq.set(1.0)  # устанавливает частоту модуляции в 1 Гц
    modulation_depth.set(0.5)  # устанавливает глубину модуляции в 0.5
    
    # Обновляем ползунки
    carrier_freq_scale.set(10.0)  # устанавливает положение ползунка несущей частоты
    carrier_amp_scale.set(1.0)  # устанавливает положение ползунка амплитуды
    modulation_freq_scale.set(1.0)  # устанавливает положение ползунка частоты модуляции
    modulation_depth_scale.set(0.5)  # устанавливает положение ползунка глубины модуляции
    
    # Обновляем графики
    update_plots()  # вызывает функцию обновления графиков с новыми параметрами

# Создаем основной фрейм для элементов управления
control_frame = tk.Frame(root)  # создает контейнер для элементов управления
control_frame.pack(pady=10)  # размещает контейнер с вертикальными отступами

# Создаем фрейм для параметров несущей
carrier_frame = tk.LabelFrame(control_frame, text="Параметры несущей", font=('Arial', 10, 'bold'))  # создает группу для параметров несущей
carrier_frame.grid(row=0, column=0, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Несущая частота
carrier_freq_label = tk.Label(carrier_frame, text="Несущая частота (Гц):")  # создает метку для несущей частоты
carrier_freq_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')  # размещает метку

carrier_freq_scale = tk.Scale(carrier_frame, from_=1, to=50, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для несущей частоты
                             variable=carrier_freq, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                             length=200)  # устанавливает длину ползунка
carrier_freq_scale.set(10.0)  # устанавливает начальное значение ползунка
carrier_freq_scale.grid(row=0, column=1, padx=5, pady=2)  # размещает ползунок

carrier_freq_value = tk.Label(carrier_frame, textvariable=carrier_freq, width=5)  # создает метку для отображения текущего значения
carrier_freq_value.grid(row=0, column=2, padx=5, pady=2)  # размещает метку значения

# Амплитуда несущей
carrier_amp_label = tk.Label(carrier_frame, text="Амплитуда несущей:")  # создает метку для амплитуды несущей
carrier_amp_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')  # размещает метку

carrier_amp_scale = tk.Scale(carrier_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для амплитуды
                            variable=carrier_amp, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                            length=200)  # устанавливает длину ползунка
carrier_amp_scale.set(1.0)  # устанавливает начальное значение
carrier_amp_scale.grid(row=1, column=1, padx=5, pady=2)  # размещает ползунок

carrier_amp_value = tk.Label(carrier_frame, textvariable=carrier_amp, width=5)  # создает метку для отображения значения
carrier_amp_value.grid(row=1, column=2, padx=5, pady=2)  # размещает метку значения

# Создаем фрейм для параметров модуляции
modulation_frame = tk.LabelFrame(control_frame, text="Параметры модуляции", font=('Arial', 10, 'bold'))  # создает группу для параметров модуляции
modulation_frame.grid(row=0, column=1, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Частота модуляции
modulation_freq_label = tk.Label(modulation_frame, text="Частота модуляции (Гц):")  # создает метку для частоты модуляции
modulation_freq_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')  # размещает метку

modulation_freq_scale = tk.Scale(modulation_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для частоты модуляции
                                variable=modulation_freq, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                                length=200)  # устанавливает длину ползунка
modulation_freq_scale.set(1.0)  # устанавливает начальное значение
modulation_freq_scale.grid(row=0, column=1, padx=5, pady=2)  # размещает ползунок

modulation_freq_value = tk.Label(modulation_frame, textvariable=modulation_freq, width=5)  # создает метку для отображения значения
modulation_freq_value.grid(row=0, column=2, padx=5, pady=2)  # размещает метку значения

# Глубина модуляции
modulation_depth_label = tk.Label(modulation_frame, text="Глубина модуляции:")  # создает метку для глубины модуляции
modulation_depth_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')  # размещает метку

modulation_depth_scale = tk.Scale(modulation_frame, from_=0.1, to=1.0, resolution=0.05, orient=tk.HORIZONTAL,  # создает ползунок для глубины модуляции
                                 variable=modulation_depth, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                                 length=200)  # устанавливает длину ползунка
modulation_depth_scale.set(0.5)  # устанавливает начальное значение
modulation_depth_scale.grid(row=1, column=1, padx=5, pady=2)  # размещает ползунок

modulation_depth_value = tk.Label(modulation_frame, textvariable=modulation_depth, width=5)  # создает метку для отображения значения
modulation_depth_value.grid(row=1, column=2, padx=5, pady=2)  # размещает метку значения

# Создаем фрейм для кнопок
button_frame = tk.Frame(control_frame)  # создает контейнер для кнопок
button_frame.grid(row=0, column=2, padx=10, pady=5)  # размещает контейнер в сетке

# Кнопка сброса
reset_button = tk.Button(button_frame, text="Сбросить параметры", command=reset_parameters,  # создает кнопку сброса
                        bg="lightcoral", width=15, height=2)  # устанавливает цвет фона и размер
reset_button.pack(pady=5)  # размещает кнопку

# Кнопка обновления
update_button = tk.Button(button_frame, text="Обновить графики", command=update_plots,  # создает кнопку обновления
                         bg="lightgreen", width=15, height=2)  # устанавливает цвет фона и размер
update_button.pack(pady=5)  # размещает кнопку

# Создаем фигуру matplotlib с 4 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))  # создает фигуру с 4 графиками (2x2)
fig.tight_layout(pad=4.0)  # автоматически регулирует отступы между графиками

# Создаем холст для встраивания графиков в tkinter
canvas = FigureCanvasTkAgg(fig, master=root)  # создает холст для отображения matplotlib графиков в tkinter
canvas_widget = canvas.get_tk_widget()  # получает tkinter-виджет из холста
canvas_widget.pack(pady=10)  # размещает виджет с графиками в окне

# Создаем текстовое поле для информации
info_text = tk.Text(root, height=8, width=80, font=('Courier New', 9))  # создает текстовое поле для информации
info_text.pack(pady=10)  # размещает текстовое поле в окне

# Создаем метку с инструкциями
instruction_label = tk.Label(root, text="Используйте ползунки для изменения параметров амплитудной модуляции", 
                            font=('Arial', 10), fg='blue')  # создает метку с инструкциями
instruction_label.pack(pady=5)  # размещает метку

# Инициализируем графики с начальными параметрами
update_plots()  # вызывает функцию обновления графиков для построения начальных графиков

# Запускаем главный цикл обработки событий
root.mainloop()  # запускает бесконечный цикл обработки событий tkinter