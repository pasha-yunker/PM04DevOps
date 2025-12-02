# Импорт необходимых библиотек
import tkinter as tk  # импортирует библиотеку tkinter для создания графического интерфейса
from tkinter import ttk  # импортирует модуль ttk для стилизованных виджетов
import numpy as np  # импортирует библиотеку numpy для математических операций с массивами
import matplotlib.pyplot as plt  # импортирует библиотеку matplotlib для построения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # импортирует класс для встраивания графиков в tkinter

# Создаем главное окно приложения
root = tk.Tk()  # создает главное окно приложения
root.title("Цифровая модуляция: ASK, FSK, PSK | Работа Павла Юнкер")  # устанавливает заголовок окна
root.geometry("1200x900")  # устанавливает размер окна 1200x900 пикселей

# Глобальные переменные для параметров модуляции
carrier_freq = tk.DoubleVar(value=5.0)  # создает переменную для несущей частоты с начальным значением 5 Гц
bit_rate = tk.DoubleVar(value=1.0)  # создает переменную для скорости передачи данных с начальным значением 1 бит/с
amplitude_1 = tk.DoubleVar(value=1.0)  # создает переменную для амплитуды бита '1' в ASK
amplitude_0 = tk.DoubleVar(value=0.0)  # создает переменную для амплитуды бита '0' в ASK
freq_1 = tk.DoubleVar(value=8.0)  # создает переменную для частоты бита '1' в FSK
freq_0 = tk.DoubleVar(value=2.0)  # создает переменную для частоты бита '0' в FSK
phase_1 = tk.DoubleVar(value=0.0)  # создает переменную для фазы бита '1' в PSK (0 градусов)
phase_0 = tk.DoubleVar(value=180.0)  # создает переменную для фазы бита '0' в PSK (180 градусов)
binary_data = tk.StringVar(value="10110010")  # создает переменную для битовой последовательности

# Функция для генерации цифрового сигнала данных
def generate_digital_signal(bits, bit_duration, samples_per_bit):
    """
    Функция для генерации цифрового сигнала из битовой последовательности
    """
    digital_signal = []  # создает пустой список для цифрового сигнала
    time_signal = []  # создает пустой список для временных меток
    
    for bit in bits:  # цикл по каждому биту в последовательности
        bit_value = int(bit)  # преобразует символ бита в целое число (0 или 1)
        # Генерируем сигнал для одного бита
        t_bit = np.linspace(0, bit_duration, samples_per_bit)  # создает массив времени для одного бита
        digital_signal.extend([bit_value] * samples_per_bit)  # добавляет samples_per_bit отсчетов текущего бита
        if time_signal:  # если массив времени уже не пустой
            last_time = time_signal[-1]  # получает последнее значение времени
            time_signal.extend(last_time + t_bit)  # добавляет новые временные метки с учетом предыдущих
        else:  # если массив времени пустой (первый бит)
            time_signal.extend(t_bit)  # добавляет временные метки от 0 до bit_duration
    
    return np.array(time_signal), np.array(digital_signal)  # возвращает массивы времени и цифрового сигнала

# Функция для ASK модуляции (Amplitude Shift Keying)
def ask_modulation(digital_signal, t, fc, amp1, amp0):
    """
    Функция для амплитудной манипуляции (ASK)
    """
    carrier = np.cos(2 * np.pi * fc * t)  # генерирует несущий сигнал cos(2πfc*t)
    ask_signal = np.zeros_like(t)  # создает массив нулей такой же длины как t для ASK сигнала
    
    for i in range(len(digital_signal)):  # цикл по всем отсчетам цифрового сигнала
        if digital_signal[i] == 1:  # если текущий бит равен 1
            ask_signal[i] = amp1 * carrier[i]  # умножает несущую на амплитуду для бита 1
        else:  # если текущий бит равен 0
            ask_signal[i] = amp0 * carrier[i]  # умножает несущую на амплитуду для бита 0
    
    return ask_signal  # возвращает ASK модулированный сигнал

# Функция для FSK модуляции (Frequency Shift Keying)
def fsk_modulation(digital_signal, t, fc1, fc0):
    """
    Функция для частотной манипуляции (FSK)
    """
    fsk_signal = np.zeros_like(t)  # создает массив нулей такой же длины как t для FSK сигнала
    
    for i in range(len(digital_signal)):  # цикл по всем отсчетам цифрового сигнала
        if digital_signal[i] == 1:  # если текущий бит равен 1
            fsk_signal[i] = np.cos(2 * np.pi * fc1 * t[i])  # генерирует сигнал с частотой для бита 1
        else:  # если текущий бит равен 0
            fsk_signal[i] = np.cos(2 * np.pi * fc0 * t[i])  # генерирует сигнал с частотой для бита 0
    
    return fsk_signal  # возвращает FSK модулированный сигнал

# Функция для PSK модуляции (Phase Shift Keying)
def psk_modulation(digital_signal, t, fc, phase1, phase0):
    """
    Функция для фазовой манипуляции (PSK)
    """
    # Преобразуем фазы из градусов в радианы
    phase1_rad = np.deg2rad(phase1)  # преобразует фазу для бита 1 из градусов в радианы
    phase0_rad = np.deg2rad(phase0)  # преобразует фазу для бита 0 из градусов в радианы
    
    psk_signal = np.zeros_like(t)  # создает массив нулей такой же длины как t для PSK сигнала
    
    for i in range(len(digital_signal)):  # цикл по всем отсчетам цифрового сигнала
        if digital_signal[i] == 1:  # если текущий бит равен 1
            psk_signal[i] = np.cos(2 * np.pi * fc * t[i] + phase1_rad)  # генерирует сигнал с фазой для бита 1
        else:  # если текущий бит равен 0
            psk_signal[i] = np.cos(2 * np.pi * fc * t[i] + phase0_rad)  # генерирует сигнал с фазой для бита 0
    
    return psk_signal  # возвращает PSK модулированный сигнал

# Функция для обновления всех графиков
def update_plots():
    """
    Функция для обновления всех графиков при изменении параметров
    """
    # Получаем текущие значения параметров
    fc = carrier_freq.get()  # получает текущее значение несущей частоты
    br = bit_rate.get()  # получает текущее значение скорости передачи
    amp1 = amplitude_1.get()  # получает амплитуду для бита 1 в ASK
    amp0 = amplitude_0.get()  # получает амплитуду для бита 0 в ASK
    freq1 = freq_1.get()  # получает частоту для бита 1 в FSK
    freq0 = freq_0.get()  # получает частоту для бита 0 в FSK
    phase1 = phase_1.get()  # получает фазу для бита 1 в PSK
    phase0 = phase_0.get()  # получает фазу для бита 0 в PSK
    data = binary_data.get()  # получает битовую последовательность
    
    # Проверяем корректность данных
    if not all(bit in '01' for bit in data):  # проверяет, что все символы в строке - 0 или 1
        data = "10110010"  # если есть некорректные символы, устанавливает последовательность по умолчанию
        binary_data.set(data)  # обновляет переменную с данными
        data_entry.delete(0, tk.END)  # очищает поле ввода
        data_entry.insert(0, data)  # вставляет корректные данные
    
    # Параметры дискретизации
    samples_per_bit = 500  # устанавливает количество отсчетов на один бит для плавности графиков
    bit_duration = 1.0 / br  # вычисляет длительность одного бита в секундах
    total_duration = len(data) * bit_duration  # вычисляет общую длительность сигнала
    
    # Генерируем временную шкалу и цифровой сигнал
    t, digital = generate_digital_signal(data, bit_duration, samples_per_bit)  # генерирует цифровой сигнал
    
    # Вычисляем модулированные сигналы
    ask_signal = ask_modulation(digital, t, fc, amp1, amp0)  # генерирует ASK сигнал
    fsk_signal = fsk_modulation(digital, t, freq1, freq0)  # генерирует FSK сигнал
    psk_signal = psk_modulation(digital, t, fc, phase1, phase0)  # генерирует PSK сигнал
    
    # Очищаем все графики
    for ax in [ax1, ax2, ax3, ax4]:  # цикл по всем областям графиков
        ax.clear()  # очищает каждую область графика
    
    # График 1: Цифровой сигнал данных
    ax1.step(t, digital, 'r-', where='post', linewidth=2, label='Цифровой сигнал')  # строит ступенчатый график цифрового сигнала
    ax1.set_title('Цифровой сигнал данных')  # устанавливает заголовок первого графика
    ax1.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax1.set_ylabel('Уровень')  # добавляет подпись к оси Y
    ax1.set_ylim(-0.1, 1.1)  # устанавливает пределы по оси Y от -0.1 до 1.1
    ax1.grid(True, alpha=0.3)  # добавляет сетку с прозрачностью 30%
    ax1.legend()  # добавляет легенду
    
    # Добавляем подписи битов
    for i, bit in enumerate(data):  # цикл по всем битам с получением индекса и значения
        x_pos = (i + 0.5) * bit_duration  # вычисляет позицию по X для подписи бита (середина бита)
        ax1.text(x_pos, 1.05, bit, ha='center', va='bottom', fontweight='bold')  # добавляет текст бита над графиком
    
    # График 2: ASK модуляция
    ax2.plot(t, ask_signal, 'b-', linewidth=1.5, label='ASK сигнал')  # строит график ASK сигнала синим цветом
    ax2.set_title('ASK - Амплитудная манипуляция')  # устанавливает заголовок второго графика
    ax2.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax2.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax2.grid(True, alpha=0.3)  # добавляет сетку
    ax2.legend()  # добавляет легенду
    
    # График 3: FSK модуляция
    ax3.plot(t, fsk_signal, 'g-', linewidth=1.5, label='FSK сигнал')  # строит график FSK сигнала зеленым цветом
    ax3.set_title('FSK - Частотная манипуляция')  # устанавливает заголовок третьего графика
    ax3.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax3.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax3.grid(True, alpha=0.3)  # добавляет сетку
    ax3.legend()  # добавляет легенду
    
    # График 4: PSK модуляция
    ax4.plot(t, psk_signal, 'm-', linewidth=1.5, label='PSK сигнал')  # строит график PSK сигнала пурпурным цветом
    ax4.set_title('PSK - Фазовая манипуляция')  # устанавливает заголовок четвертого графика
    ax4.set_xlabel('Время (с)')  # добавляет подпись к оси X
    ax4.set_ylabel('Амплитуда')  # добавляет подпись к оси Y
    ax4.grid(True, alpha=0.3)  # добавляет сетку
    ax4.legend()  # добавляет легенду
    
    # Настраиваем внешний вид всех графиков
    for ax in [ax1, ax2, ax3, ax4]:  # цикл по всем графикам
        ax.set_xlim(0, total_duration)  # устанавливает одинаковые пределы по оси X для всех графиков
    
    # Автоматически подбираем масштаб по оси Y для модулированных сигналов
    for ax in [ax2, ax3, ax4]:  # цикл по графикам модулированных сигналов
        ax.set_ylim(-1.2, 1.2)  # устанавливает фиксированные пределы по Y для лучшего сравнения
    
    # Обновляем информацию о параметрах
    update_info_text(data, br, fc)  # вызывает функцию обновления текстовой информации
    
    # Обновляем холст с графиками
    canvas.draw()  # перерисовывает холст чтобы отобразить все изменения

# Функция для обновления текстовой информации
def update_info_text(data, br, fc):
    """
    Функция для обновления текстовой информации о параметрах модуляции
    """
    # Очищаем текстовое поле
    info_text.delete('1.0', tk.END)  # удаляет весь текст из текстового поля
    
    # Добавляем информацию о параметрах
    info_text.insert(tk.END, "Параметры цифровой модуляции:\n")  # вставляет заголовок
    info_text.insert(tk.END, "=" * 50 + "\n\n")  # добавляет разделительную линию
    
    # Информация о данных
    info_text.insert(tk.END, "Битовая последовательность:\n")  # вставляет подзаголовок
    info_text.insert(tk.END, f"Данные: {data}\n")  # выводит битовую последовательность
    info_text.insert(tk.END, f"Длина: {len(data)} бит\n\n")  # выводит длину последовательности
    
    # Основные параметры
    info_text.insert(tk.END, "Основные параметры:\n")  # вставляет подзаголовок
    info_text.insert(tk.END, f"Скорость передачи: {br} бит/с\n")  # выводит скорость передачи
    info_text.insert(tk.END, f"Длительность бита: {1.0/br:.2f} с\n")  # выводит длительность одного бита
    info_text.insert(tk.END, f"Несущая частота: {fc} Гц\n\n")  # выводит несущую частоту
    
    # Параметры ASK
    info_text.insert(tk.END, "ASK параметры:\n")  # вставляет подзаголовок для ASK
    info_text.insert(tk.END, f"  Амплитуда для '1': {amplitude_1.get():.1f}\n")  # выводит амплитуду для бита 1
    info_text.insert(tk.END, f"  Амплитуда для '0': {amplitude_0.get():.1f}\n\n")  # выводит амплитуду для бита 0
    
    # Параметры FSK
    info_text.insert(tk.END, "FSK параметры:\n")  # вставляет подзаголовок для FSK
    info_text.insert(tk.END, f"  Частота для '1': {freq_1.get():.1f} Гц\n")  # выводит частоту для бита 1
    info_text.insert(tk.END, f"  Частота для '0': {freq_0.get():.1f} Гц\n\n")  # выводит частоту для бита 0
    
    # Параметры PSK
    info_text.insert(tk.END, "PSK параметры:\n")  # вставляет подзаголовок для PSK
    info_text.insert(tk.END, f"  Фаза для '1': {phase_1.get():.0f}°\n")  # выводит фазу для бита 1
    info_text.insert(tk.END, f"  Фаза для '0': {phase_0.get():.0f}°\n\n")  # выводит фазу для бита 0

# Функция для сброса параметров к значениям по умолчанию
def reset_parameters():
    """
    Функция для сброса всех параметров к значениям по умолчанию
    """
    carrier_freq.set(5.0)  # устанавливает несущую частоту в 5 Гц
    bit_rate.set(1.0)  # устанавливает скорость передачи в 1 бит/с
    amplitude_1.set(1.0)  # устанавливает амплитуду для бита 1 в 1.0
    amplitude_0.set(0.0)  # устанавливает амплитуду для бита 0 в 0.0
    freq_1.set(8.0)  # устанавливает частоту для бита 1 в 8 Гц
    freq_0.set(2.0)  # устанавливает частоту для бита 0 в 2 Гц
    phase_1.set(0.0)  # устанавливает фазу для бита 1 в 0 градусов
    phase_0.set(180.0)  # устанавливает фазу для бита 0 в 180 градусов
    binary_data.set("10110010")  # устанавливает битовую последовательность по умолчанию
    
    # Обновляем поля ввода
    data_entry.delete(0, tk.END)  # очищает поле ввода данных
    data_entry.insert(0, "10110010")  # вставляет данные по умолчанию
    
    # Обновляем графики
    update_plots()  # вызывает функцию обновления графиков с новыми параметрами

# Функция для генерации случайной битовой последовательности
def generate_random_data():
    """
    Функция для генерации случайной битовой последовательности
    """
    import random  # импортирует модуль random для генерации случайных чисел
    length = 8  # устанавливает длину последовательности в 8 бит
    random_bits = ''.join(str(random.randint(0, 1)) for _ in range(length))  # генерирует случайную последовательность из 0 и 1
    binary_data.set(random_bits)  # устанавливает сгенерированную последовательность
    data_entry.delete(0, tk.END)  # очищает поле ввода данных
    data_entry.insert(0, random_bits)  # вставляет случайную последовательность
    update_plots()  # обновляет графики с новыми данными

# Создаем основной фрейм для элементов управления
control_frame = tk.Frame(root)  # создает контейнер для элементов управления
control_frame.pack(pady=10)  # размещает контейнер с вертикальными отступами

# Создаем фрейм для основных параметров
basic_frame = tk.LabelFrame(control_frame, text="Основные параметры", font=('Arial', 10, 'bold'))  # создает группу для основных параметров
basic_frame.grid(row=0, column=0, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Несущая частота
carrier_freq_label = tk.Label(basic_frame, text="Несущая частота (Гц):")  # создает метку для несущей частоты
carrier_freq_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')  # размещает метку

carrier_freq_scale = tk.Scale(basic_frame, from_=1, to=20, resolution=0.5, orient=tk.HORIZONTAL,  # создает ползунок для несущей частоты
                             variable=carrier_freq, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                             length=150)  # устанавливает длину ползунка
carrier_freq_scale.grid(row=0, column=1, padx=5, pady=2)  # размещает ползунок

# Скорость передачи
bit_rate_label = tk.Label(basic_frame, text="Скорость (бит/с):")  # создает метку для скорости передачи
bit_rate_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')  # размещает метку

bit_rate_scale = tk.Scale(basic_frame, from_=0.5, to=5.0, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для скорости передачи
                         variable=bit_rate, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                         length=150)  # устанавливает длину ползунка
bit_rate_scale.grid(row=1, column=1, padx=5, pady=2)  # размещает ползунок

# Поле ввода данных
data_label = tk.Label(basic_frame, text="Биты данных:")  # создает метку для поля ввода данных
data_label.grid(row=2, column=0, padx=5, pady=2, sticky='w')  # размещает метку

data_entry = tk.Entry(basic_frame, textvariable=binary_data, width=15)  # создает поле ввода для битовой последовательности
data_entry.grid(row=2, column=1, padx=5, pady=2)  # размещает поле ввода
data_entry.bind('<Return>', lambda x: update_plots())  # привязывает нажатие Enter к обновлению графиков

# Создаем фрейм для параметров ASK
ask_frame = tk.LabelFrame(control_frame, text="ASK параметры", font=('Arial', 9, 'bold'))  # создает группу для параметров ASK
ask_frame.grid(row=0, column=1, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Амплитуда для бита 1 (ASK)
amp1_label = tk.Label(ask_frame, text="Амплитуда '1':")  # создает метку для амплитуды бита 1
amp1_label.grid(row=0, column=0, padx=5, pady=1, sticky='w')  # размещает метку

amp1_scale = tk.Scale(ask_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для амплитуды бита 1
                     variable=amplitude_1, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                     length=120)  # устанавливает длину ползунка
amp1_scale.grid(row=0, column=1, padx=5, pady=1)  # размещает ползунок

# Амплитуда для бита 0 (ASK)
amp0_label = tk.Label(ask_frame, text="Амплитуда '0':")  # создает метку для амплитуды бита 0
amp0_label.grid(row=1, column=0, padx=5, pady=1, sticky='w')  # размещает метку

amp0_scale = tk.Scale(ask_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,  # создает ползунок для амплитуды бита 0
                     variable=amplitude_0, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                     length=120)  # устанавливает длину ползунка
amp0_scale.grid(row=1, column=1, padx=5, pady=1)  # размещает ползунок

# Создаем фрейм для параметров FSK
fsk_frame = tk.LabelFrame(control_frame, text="FSK параметры", font=('Arial', 9, 'bold'))  # создает группу для параметров FSK
fsk_frame.grid(row=0, column=2, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Частота для бита 1 (FSK)
freq1_label = tk.Label(fsk_frame, text="Частота '1' (Гц):")  # создает метку для частоты бита 1
freq1_label.grid(row=0, column=0, padx=5, pady=1, sticky='w')  # размещает метку

freq1_scale = tk.Scale(fsk_frame, from_=1, to=15, resolution=0.5, orient=tk.HORIZONTAL,  # создает ползунок для частоты бита 1
                      variable=freq_1, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                      length=120)  # устанавливает длину ползунка
freq1_scale.grid(row=0, column=1, padx=5, pady=1)  # размещает ползунок

# Частота для бита 0 (FSK)
freq0_label = tk.Label(fsk_frame, text="Частота '0' (Гц):")  # создает метку для частоты бита 0
freq0_label.grid(row=1, column=0, padx=5, pady=1, sticky='w')  # размещает метку

freq0_scale = tk.Scale(fsk_frame, from_=1, to=15, resolution=0.5, orient=tk.HORIZONTAL,  # создает ползунок для частоты бита 0
                      variable=freq_0, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                      length=120)  # устанавливает длину ползунка
freq0_scale.grid(row=1, column=1, padx=5, pady=1)  # размещает ползунок

# Создаем фрейм для параметров PSK
psk_frame = tk.LabelFrame(control_frame, text="PSK параметры", font=('Arial', 9, 'bold'))  # создает группу для параметров PSK
psk_frame.grid(row=0, column=3, padx=10, pady=5, sticky='ew')  # размещает группу в сетке

# Фаза для бита 1 (PSK)
phase1_label = tk.Label(psk_frame, text="Фаза '1' (°):")  # создает метку для фазы бита 1
phase1_label.grid(row=0, column=0, padx=5, pady=1, sticky='w')  # размещает метку

phase1_scale = tk.Scale(psk_frame, from_=0, to=360, resolution=45, orient=tk.HORIZONTAL,  # создает ползунок для фазы бита 1
                       variable=phase_1, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                       length=120)  # устанавливает длину ползунка
phase1_scale.grid(row=0, column=1, padx=5, pady=1)  # размещает ползунок

# Фаза для бита 0 (PSK)
phase0_label = tk.Label(psk_frame, text="Фаза '0' (°):")  # создает метку для фазы бита 0
phase0_label.grid(row=1, column=0, padx=5, pady=1, sticky='w')  # размещает метку

phase0_scale = tk.Scale(psk_frame, from_=0, to=360, resolution=45, orient=tk.HORIZONTAL,  # создает ползунок для фазы бита 0
                       variable=phase_0, command=lambda x: update_plots(),  # привязывает к переменной и функции обновления
                       length=120)  # устанавливает длину ползунка
phase0_scale.grid(row=1, column=1, padx=5, pady=1)  # размещает ползунок

# Создаем фрейм для кнопок
button_frame = tk.Frame(control_frame)  # создает контейнер для кнопок
button_frame.grid(row=0, column=4, padx=10, pady=5)  # размещает контейнер в сетке

# Кнопка сброса
reset_button = tk.Button(button_frame, text="Сбросить", command=reset_parameters,  # создает кнопку сброса
                        bg="lightcoral", width=12, height=1)  # устанавливает цвет фона и размер
reset_button.pack(pady=2)  # размещает кнопку

# Кнопка случайных данных
random_button = tk.Button(button_frame, text="Случайные данные", command=generate_random_data,  # создает кнопку для генерации случайных данных
                         bg="lightyellow", width=12, height=1)  # устанавливает цвет фона и размер
random_button.pack(pady=2)  # размещает кнопку

# Кнопка обновления
update_button = tk.Button(button_frame, text="Обновить", command=update_plots,  # создает кнопку обновления
                         bg="lightgreen", width=12, height=1)  # устанавливает цвет фона и размер
update_button.pack(pady=2)  # размещает кнопку

# Создаем фигуру matplotlib с 4 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))  # создает фигуру с 4 графиками (2x2)
fig.tight_layout(pad=4.0)  # автоматически регулирует отступы между графиками

# Создаем холст для встраивания графиков в tkinter
canvas = FigureCanvasTkAgg(fig, master=root)  # создает холст для отображения matplotlib графиков в tkinter
canvas_widget = canvas.get_tk_widget()  # получает tkinter-виджет из холста
canvas_widget.pack(pady=10)  # размещает виджет с графиками в окне

# Создаем текстовое поле для информации
info_text = tk.Text(root, height=10, width=100, font=('Courier New', 9))  # создает текстовое поле для информации
info_text.pack(pady=10)  # размещает текстовое поле в окне

# Создаем метку с инструкциями
instruction_label = tk.Label(root, text="Измените параметры с помощью ползунков и введите свою битовую последовательность (только 0 и 1)", 
                            font=('Arial', 10), fg='blue')  # создает метку с инструкциями
instruction_label.pack(pady=5)  # размещает метку

# Инициализируем графики с начальными параметрами
update_plots()  # вызывает функцию обновления графиков для построения начальных графиков

# Запускаем главный цикл обработки событий
root.mainloop()  # запускает бесконечный цикл обработки событий tkinter