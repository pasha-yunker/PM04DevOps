import tkinter as tk
from tkinter import ttk, Scale
import math
import random
import time

class AdvancedSignalGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎛️ ПРОФЕССИОНАЛЬНЫЙ ГЕНЕРАТОР СИГНАЛОВ СТЕРЕО | Работа Павла Юнкер")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Параметры сигнала для левого и правого каналов
        self.left_channel = {
            'amplitude': 1000,  # mV
            'frequency': 1000.0,
            'phase': 0.0,
            'enabled': True
        }
        
        self.right_channel = {
            'amplitude': 1000,  # mV
            'frequency': 1000.0,
            'phase': 0.0,
            'enabled': True
        }
        
        self.signal_type = "sine"
        self.is_playing = True
        self.master_volume = 1.0
        self.time_offset = 0
        
        self.setup_ui()
        self.animate()
        
    def setup_ui(self):
        # Главный контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Верхняя панель - мастер контролы
        self.create_master_controls(main_container)
        
        # Центральная область - каналы и график
        center_frame = ttk.Frame(main_container)
        center_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Левый канал
        self.left_frame = self.create_channel_control(center_frame, "🔴 ЛЕВЫЙ КАНАЛ", "left")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # График
        self.setup_plot(center_frame)
        
        # Правый канал
        self.right_frame = self.create_channel_control(center_frame, "🔵 ПРАВЫЙ КАНАЛ", "right")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Нижняя панель - управление
        self.create_control_panel(main_container)
        
    def create_master_controls(self, parent):
        master_frame = ttk.LabelFrame(parent, text="🎛️ МАСТЕР КОНТРОЛЬ")
        master_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Тип сигнала
        type_frame = ttk.Frame(master_frame)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(type_frame, text="Форма сигнала:", style='Title.TLabel').pack(side=tk.LEFT)
        
        self.type_var = tk.StringVar(value="Синус")
        types = ["Синус", "Прямоугольный", "Пилообразный", "Треугольный", "Шум"]
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, values=types, 
                                 state="readonly", width=15)
        type_combo.pack(side=tk.LEFT, padx=10)
        type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Мастер громкость
        volume_frame = ttk.Frame(master_frame)
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(volume_frame, text="Мастер громкость:", style='Title.TLabel').pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=1.0)
        volume_scale = Scale(volume_frame, from_=0.0, to=1.0, resolution=0.01,
                           orient=tk.HORIZONTAL, variable=self.volume_var,
                           length=200, showvalue=True,
                           command=self.on_volume_change)
        volume_scale.pack(side=tk.LEFT, padx=10)
        
        self.volume_value = ttk.Label(volume_frame, text="100%")
        self.volume_value.pack(side=tk.LEFT, padx=10)
        
    def create_channel_control(self, parent, title, channel):
        frame = ttk.LabelFrame(parent, text=title)
        
        # Индикатор уровня
        level_frame = ttk.Frame(frame)
        level_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(level_frame, text="Уровень:").pack()
        
        # Анимированный индикатор уровня
        self.canvas_level = tk.Canvas(level_frame, width=200, height=30, bg='#1a1a1a', highlightthickness=0)
        self.canvas_level.pack(pady=5)
        
        # Амплитуда в mV
        amp_frame = ttk.Frame(frame)
        amp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(amp_frame, text="Амплитуда (mV):").pack()
        
        amp_var = tk.IntVar(value=1000)
        amp_scale = Scale(amp_frame, from_=0, to=5000, resolution=10,
                         orient=tk.HORIZONTAL, variable=amp_var,
                         length=200, showvalue=True,
                         command=lambda v: self.on_amplitude_change(v, channel))
        amp_scale.pack(pady=5)
        
        # Сохраняем ссылки на переменные
        if channel == 'left':
            self.left_amp_var = amp_var
        else:
            self.right_amp_var = amp_var
        
        # Прецизионные регуляторы частоты
        self.create_frequency_controls(frame, channel)
        
        # Фаза
        phase_frame = ttk.Frame(frame)
        phase_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(phase_frame, text="Фаза (°):").pack()
        
        phase_var = tk.DoubleVar(value=0.0)
        phase_scale = Scale(phase_frame, from_=0, to=360, resolution=1,
                           orient=tk.HORIZONTAL, variable=phase_var,
                           length=200, showvalue=True,
                           command=lambda v: self.on_phase_change(v, channel))
        phase_scale.pack(pady=5)
        
        # Сохраняем ссылки
        if channel == 'left':
            self.left_phase_var = phase_var
        else:
            self.right_phase_var = phase_var
        
        # Включение/выключение канала
        enable_frame = ttk.Frame(frame)
        enable_frame.pack(fill=tk.X, padx=10, pady=10)
        
        enable_var = tk.BooleanVar(value=True)
        enable_btn = ttk.Checkbutton(enable_frame, text="Включен", 
                                   variable=enable_var,
                                   command=lambda: self.on_channel_toggle(channel, enable_var))
        enable_btn.pack()
        
        # Сохраняем ссылки
        if channel == 'left':
            self.left_enable_var = enable_var
        else:
            self.right_enable_var = enable_var
        
        return frame
        
    def create_frequency_controls(self, parent, channel):
        freq_frame = ttk.LabelFrame(parent, text="🎚️ ЧАСТОТА")
        freq_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Основная частота
        main_freq_frame = ttk.Frame(freq_frame)
        main_freq_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(main_freq_frame, text="Основная:").pack(side=tk.LEFT)
        
        main_freq_var = tk.DoubleVar(value=1000.0)
        main_freq_scale = Scale(main_freq_frame, from_=20, to=20000, resolution=1,
                               orient=tk.HORIZONTAL, variable=main_freq_var,
                               length=180, showvalue=True,
                               command=lambda v: self.on_main_frequency_change(v, channel))
        main_freq_scale.pack(side=tk.RIGHT)
        
        # Прецизионные регуляторы
        precision_frame = ttk.Frame(freq_frame)
        precision_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 1 kHz регулятор
        kHz_frame = ttk.Frame(precision_frame)
        kHz_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(kHz_frame, text="1 kHz:", width=8).pack(side=tk.LEFT)
        khz_var = tk.IntVar(value=1)
        khz_scale = Scale(kHz_frame, from_=0, to=20, resolution=1,
                         orient=tk.HORIZONTAL, variable=khz_var,
                         length=150, showvalue=False,
                         command=lambda v: self.on_khz_change(v, channel))
        khz_scale.pack(side=tk.RIGHT)
        khz_label = ttk.Label(kHz_frame, text="1 kHz", width=8)
        khz_label.pack(side=tk.RIGHT)
        
        # 100 Hz регулятор
        hz100_frame = ttk.Frame(precision_frame)
        hz100_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(hz100_frame, text="100 Hz:", width=8).pack(side=tk.LEFT)
        hz100_var = tk.IntVar(value=0)
        hz100_scale = Scale(hz100_frame, from_=0, to=9, resolution=1,
                           orient=tk.HORIZONTAL, variable=hz100_var,
                           length=150, showvalue=False,
                           command=lambda v: self.on_hz100_change(v, channel))
        hz100_scale.pack(side=tk.RIGHT)
        hz100_label = ttk.Label(hz100_frame, text="0 Hz", width=8)
        hz100_label.pack(side=tk.RIGHT)
        
        # 1 Hz регулятор
        hz1_frame = ttk.Frame(precision_frame)
        hz1_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(hz1_frame, text="1 Hz:", width=8).pack(side=tk.LEFT)
        hz1_var = tk.IntVar(value=0)
        hz1_scale = Scale(hz1_frame, from_=0, to=99, resolution=1,
                         orient=tk.HORIZONTAL, variable=hz1_var,
                         length=150, showvalue=False,
                         command=lambda v: self.on_hz1_change(v, channel))
        hz1_scale.pack(side=tk.RIGHT)
        hz1_label = ttk.Label(hz1_frame, text="0 Hz", width=8)
        hz1_label.pack(side=tk.RIGHT)
        
        # Общая частота
        total_freq_frame = ttk.Frame(freq_frame)
        total_freq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(total_freq_frame, text="Итоговая частота:").pack(side=tk.LEFT)
        total_freq_label = ttk.Label(total_freq_frame, text="1000.0 Hz")
        total_freq_label.pack(side=tk.RIGHT)
        
        # Сохраняем ссылки на переменные
        if channel == 'left':
            self.left_main_freq_var = main_freq_var
            self.left_khz_var = khz_var
            self.left_hz100_var = hz100_var
            self.left_hz1_var = hz1_var
            self.left_khz_label = khz_label
            self.left_hz100_label = hz100_label
            self.left_hz1_label = hz1_label
            self.left_total_freq_label = total_freq_label
        else:
            self.right_main_freq_var = main_freq_var
            self.right_khz_var = khz_var
            self.right_hz100_var = hz100_var
            self.right_hz1_var = hz1_var
            self.right_khz_label = khz_label
            self.right_hz100_label = hz100_label
            self.right_hz1_label = hz1_label
            self.right_total_freq_label = total_freq_label
        
    def setup_plot(self, parent):
        plot_frame = ttk.Frame(parent)
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Создаем два канваса для графиков
        self.canvas1 = tk.Canvas(plot_frame, width=600, height=200, bg='#1a1a1a', highlightthickness=1, highlightbackground='#444')
        self.canvas1.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.canvas2 = tk.Canvas(plot_frame, width=600, height=200, bg='#1a1a1a', highlightthickness=1, highlightbackground='#444')
        self.canvas2.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Заголовки для графиков
        self.canvas1.create_text(300, 20, text="🔴 ЛЕВЫЙ КАНАЛ", fill='#ff4444', font=('Arial', 12, 'bold'))
        self.canvas2.create_text(300, 20, text="🔵 ПРАВЫЙ КАНАЛ", fill='#4444ff', font=('Arial', 12, 'bold'))
        
    def create_control_panel(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Кнопки управления
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(pady=10)
        
        # Анимированные кнопки
        self.play_btn = tk.Button(btn_frame, text="⏸️ ПАУЗА", font=('Arial', 12, 'bold'),
                                 bg='#ff4444', fg='white', relief='raised', bd=3,
                                 command=self.toggle_animation, width=15, height=2)
        self.play_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(btn_frame, text="🔄 СБРОС", font=('Arial', 12, 'bold'),
                             bg='#4444ff', fg='white', relief='raised', bd=3,
                             command=self.reset_parameters, width=15, height=2)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        sync_btn = tk.Button(btn_frame, text="⚡ СИНХРОНИЗИРОВАТЬ", font=('Arial', 12, 'bold'),
                            bg='#44ff44', fg='black', relief='raised', bd=3,
                            command=self.sync_channels, width=20, height=2)
        sync_btn.pack(side=tk.LEFT, padx=10)
        
    def generate_signal(self, x, channel):
        """Генерация сигнала для указанного канала"""
        if channel == 'left':
            if not self.left_enable_var.get():
                return 0
            freq = self.left_channel['frequency']
            phase = self.left_channel['phase']
            amplitude = self.left_channel['amplitude'] * self.master_volume / 1000.0
        else:
            if not self.right_enable_var.get():
                return 0
            freq = self.right_channel['frequency']
            phase = self.right_channel['phase']
            amplitude = self.right_channel['amplitude'] * self.master_volume / 1000.0
            
        # Учитываем фазу
        x_phase = x + phase / (360 * freq)
        
        if self.signal_type == "sine":
            return amplitude * math.sin(2 * math.pi * freq * x_phase) * 1000
        elif self.signal_type == "square":
            return amplitude * (1 if math.sin(2 * math.pi * freq * x_phase) >= 0 else -1) * 1000
        elif self.signal_type == "sawtooth":
            return amplitude * (2 * (x_phase * freq - math.floor(0.5 + x_phase * freq))) * 1000
        elif self.signal_type == "triangle":
            return amplitude * (2 * abs(2 * (x_phase * freq - math.floor(x_phase * freq + 0.5))) - 1) * 1000
        elif self.signal_type == "noise":
            return amplitude * random.uniform(-1, 1) * 1000
        
    def animate(self):
        if self.is_playing:
            # Очищаем графики
            self.canvas1.delete("signal")
            self.canvas2.delete("signal")
            
            width = 600
            height = 200
            center_y = height // 2
            
            # Рисуем оси
            self.canvas1.create_line(0, center_y, width, center_y, fill="#444", tags="axis")
            self.canvas2.create_line(0, center_y, width, center_y, fill="#444", tags="axis")
            
            # Генерируем и рисуем сигналы
            points_left = []
            points_right = []
            
            for x in range(width):
                # Время с анимацией
                t = (x / width * 0.01) + self.time_offset
                
                # Левый канал
                y_left = self.generate_signal(t, 'left')
                pixel_y_left = center_y - (y_left * 0.05)  # Масштабируем
                points_left.append((x, pixel_y_left))
                
                # Правый канал
                y_right = self.generate_signal(t, 'right')
                pixel_y_right = center_y - (y_right * 0.05)  # Масштабируем
                points_right.append((x, pixel_y_right))
            
            # Рисуем линии сигналов
            if points_left:
                self.canvas1.create_line(points_left, fill="#ff4444", width=2, tags="signal")
            if points_right:
                self.canvas2.create_line(points_right, fill="#4444ff", width=2, tags="signal")
            
            self.time_offset += 0.0005
        
        # Продолжаем анимацию
        self.root.after(30, self.animate)
    
    def on_type_change(self, event):
        type_map = {
            "Синус": "sine",
            "Прямоугольный": "square",
            "Пилообразный": "sawtooth",
            "Треугольный": "triangle",
            "Шум": "noise"
        }
        self.signal_type = type_map[self.type_var.get()]
    
    def on_volume_change(self, value):
        self.master_volume = float(value)
        self.volume_value.config(text=f"{int(self.master_volume * 100)}%")
    
    def on_amplitude_change(self, value, channel):
        amplitude = int(value)
        if channel == 'left':
            self.left_channel['amplitude'] = amplitude
        else:
            self.right_channel['amplitude'] = amplitude
    
    def on_phase_change(self, value, channel):
        phase = float(value)
        if channel == 'left':
            self.left_channel['phase'] = phase
        else:
            self.right_channel['phase'] = phase
    
    def on_main_frequency_change(self, value, channel):
        freq = float(value)
        if channel == 'left':
            self.left_channel['frequency'] = freq
            self.update_frequency_display('left')
        else:
            self.right_channel['frequency'] = freq
            self.update_frequency_display('right')
    
    def on_khz_change(self, value, channel):
        khz = int(value)
        if channel == 'left':
            base_freq = self.left_channel['frequency']
            new_freq = khz * 1000 + (base_freq % 1000)
            self.left_channel['frequency'] = new_freq
            self.left_main_freq_var.set(new_freq)
            self.update_frequency_display('left')
        else:
            base_freq = self.right_channel['frequency']
            new_freq = khz * 1000 + (base_freq % 1000)
            self.right_channel['frequency'] = new_freq
            self.right_main_freq_var.set(new_freq)
            self.update_frequency_display('right')
    
    def on_hz100_change(self, value, channel):
        hz100 = int(value)
        if channel == 'left':
            base_freq = self.left_channel['frequency']
            new_freq = (base_freq // 1000) * 1000 + hz100 * 100 + (base_freq % 100)
            self.left_channel['frequency'] = new_freq
            self.left_main_freq_var.set(new_freq)
            self.update_frequency_display('left')
        else:
            base_freq = self.right_channel['frequency']
            new_freq = (base_freq // 1000) * 1000 + hz100 * 100 + (base_freq % 100)
            self.right_channel['frequency'] = new_freq
            self.right_main_freq_var.set(new_freq)
            self.update_frequency_display('right')
    
    def on_hz1_change(self, value, channel):
        hz1 = int(value)
        if channel == 'left':
            base_freq = self.left_channel['frequency']
            new_freq = (base_freq // 100) * 100 + hz1
            self.left_channel['frequency'] = new_freq
            self.left_main_freq_var.set(new_freq)
            self.update_frequency_display('left')
        else:
            base_freq = self.right_channel['frequency']
            new_freq = (base_freq // 100) * 100 + hz1
            self.right_channel['frequency'] = new_freq
            self.right_main_freq_var.set(new_freq)
            self.update_frequency_display('right')
    
    def update_frequency_display(self, channel):
        if channel == 'left':
            freq = self.left_channel['frequency']
            khz_var = self.left_khz_var
            hz100_var = self.left_hz100_var
            hz1_var = self.left_hz1_var
            khz_label = self.left_khz_label
            hz100_label = self.left_hz100_label
            hz1_label = self.left_hz1_label
            total_label = self.left_total_freq_label
        else:
            freq = self.right_channel['frequency']
            khz_var = self.right_khz_var
            hz100_var = self.right_hz100_var
            hz1_var = self.right_hz1_var
            khz_label = self.right_khz_label
            hz100_label = self.right_hz100_label
            hz1_label = self.right_hz1_label
            total_label = self.right_total_freq_label
        
        # Обновляем прецизионные регуляторы
        khz = int(freq // 1000)
        hz100 = int((freq % 1000) // 100)
        hz1 = int(freq % 100)
        
        khz_var.set(khz)
        hz100_var.set(hz100)
        hz1_var.set(hz1)
        khz_label.config(text=f"{khz} kHz")
        hz100_label.config(text=f"{hz100*100} Hz")
        hz1_label.config(text=f"{hz1} Hz")
        total_label.config(text=f"{freq:.1f} Hz")
    
    def on_channel_toggle(self, channel, enable_var):
        if channel == 'left':
            self.left_channel['enabled'] = enable_var.get()
        else:
            self.right_channel['enabled'] = enable_var.get()
    
    def toggle_animation(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.config(text="⏸️ ПАУЗА", bg='#ff4444')
        else:
            self.play_btn.config(text="▶️ ВОСПРОИЗВЕСТИ", bg='#44ff44')
    
    def reset_parameters(self):
        # Сброс всех параметров
        self.left_channel = {'amplitude': 1000, 'frequency': 1000.0, 'phase': 0.0, 'enabled': True}
        self.right_channel = {'amplitude': 1000, 'frequency': 1000.0, 'phase': 0.0, 'enabled': True}
        self.master_volume = 1.0
        self.volume_var.set(1.0)
        self.volume_value.config(text="100%")
        self.time_offset = 0
        
        # Обновление UI
        self.left_amp_var.set(1000)
        self.right_amp_var.set(1000)
        self.left_phase_var.set(0)
        self.right_phase_var.set(0)
        self.left_main_freq_var.set(1000)
        self.right_main_freq_var.set(1000)
        self.left_enable_var.set(True)
        self.right_enable_var.set(True)
        
        self.update_frequency_display('left')
        self.update_frequency_display('right')
    
    def sync_channels(self):
        # Синхронизация каналов - правый канал копирует левый
        self.right_channel['frequency'] = self.left_channel['frequency']
        self.right_channel['amplitude'] = self.left_channel['amplitude']
        self.right_channel['phase'] = self.left_channel['phase']
        
        self.right_amp_var.set(self.left_channel['amplitude'])
        self.right_phase_var.set(self.left_channel['phase'])
        self.right_main_freq_var.set(self.left_channel['frequency'])
        
        self.update_frequency_display('right')

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedSignalGenerator(root)
    root.mainloop()