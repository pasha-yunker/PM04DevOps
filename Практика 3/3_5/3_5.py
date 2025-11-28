import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Process Monitor")
        self.root.geometry("900x600")
        self.root.configure(bg='#1a1a1a')
        
        self.setup_ui()
        self.generate_sample_data()
        self.update_display()
    
    def setup_ui(self):
        # Заголовок с кнопкой справки
        header = tk.Frame(self.root, bg='#2a2a2a', height=80)
        header.pack(fill=tk.X, padx=15, pady=10)
        header.pack_propagate(False)
        
        # Левая часть заголовка - название
        title_frame = tk.Frame(header, bg='#2a2a2a')
        title_frame.pack(side=tk.LEFT, expand=True)
        
        title = tk.Label(title_frame, text="🔬 СИСТЕМА МОНИТОРИНГА ПРОЦЕССОВ", 
                        font=('Arial', 16, 'bold'), fg='white', bg='#2a2a2a')
        title.pack(anchor='w')
        
        subtitle = tk.Label(title_frame, text="Реальное время • Статус процессов • Контроль качества", 
                           font=('Arial', 9), fg='#cccccc', bg='#2a2a2a')
        subtitle.pack(anchor='w', pady=(2, 0))
        
        # Правая часть заголовка - кнопка справки
        help_button = tk.Button(header, text="❓ Справка", font=('Arial', 9),
                               bg='#3498db', fg='white', relief=tk.FLAT,
                               command=self.show_help)
        help_button.pack(side=tk.RIGHT, padx=10)
        
        # Основной контейнер для карточек
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем сетку 3x2
        self.create_card_grid(main_container)
        
        # Статус бар
        self.status_bar = tk.Frame(self.root, bg='#333333', height=25)
        self.status_bar.pack(fill=tk.X, padx=15, pady=(5, 10))
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, text="Система активна • Все процессы в норме", 
                                    font=('Arial', 8), fg='#00ff88', bg='#333333')
        self.status_label.pack(expand=True)
    
    def create_card_grid(self, parent):
        # Сетка 3 строки × 2 колонки
        for row in range(3):
            parent.grid_rowconfigure(row, weight=1)
            for col in range(2):
                parent.grid_columnconfigure(col, weight=1)
                
                card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=1)
                card_frame.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
                
                # Создаем карточку
                if row == 0 and col == 0:
                    self.create_tests_card(card_frame)
                elif row == 0 and col == 1:
                    self.create_qc_card(card_frame)
                elif row == 1 and col == 0:
                    self.create_reagents_card(card_frame)
                elif row == 1 and col == 1:
                    self.create_calibration_card(card_frame)
                elif row == 2 and col == 0:
                    self.create_supplies_card(card_frame)
                else:
                    self.create_process_path_card(card_frame)
    
    def create_tests_card(self, parent):
        # Заголовок карточки
        header = tk.Frame(parent, bg='#3498db', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧪 TESTS IN PROCESS", font=('Arial', 9, 'bold'),
                fg='white', bg='#3498db').pack(expand=True)
        
        # Содержимое
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Большой индикатор
        self.tests_value = tk.Label(content, text="", font=('Arial', 32, 'bold'),
                                  fg='#3498db', bg='#2a2a2a')
        self.tests_value.pack(expand=True)
        
        # Подпись (только "активных тестов")
        tk.Label(content, text="активных тестов", font=('Arial', 9),
                fg='#cccccc', bg='#2a2a2a').pack()
        
        # Статус (убрал прогресс бар, оставил только статус)
        self.tests_status = tk.Label(content, text="", font=('Arial', 8),
                                   fg='#cccccc', bg='#2a2a2a')
        self.tests_status.pack(pady=5)
    
    def create_qc_card(self, parent):
        header = tk.Frame(parent, bg='#9b59b6', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 QUALITY CONTROL", font=('Arial', 9, 'bold'),
                fg='white', bg='#9b59b6').pack(expand=True)
        
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Холст для графика
        self.qc_canvas = tk.Canvas(content, width=180, height=80, bg='#2a2a2a',
                                  highlightthickness=0)
        self.qc_canvas.pack(expand=True)
        
        # Показатели качества
        metrics_frame = tk.Frame(content, bg='#2a2a2a')
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.qc_accuracy = tk.Label(metrics_frame, text="", font=('Arial', 8),
                                  fg='#9b59b6', bg='#2a2a2a')
        self.qc_accuracy.pack(side=tk.LEFT)
        
        self.qc_consistency = tk.Label(metrics_frame, text="", font=('Arial', 8),
                                     fg='#9b59b6', bg='#2a2a2a')
        self.qc_consistency.pack(side=tk.RIGHT)
    
    def create_reagents_card(self, parent):
        header = tk.Frame(parent, bg='#27ae60', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧴 REAGENTS STATUS", font=('Arial', 9, 'bold'),
                fg='white', bg='#27ae60').pack(expand=True)
        
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Большой эмодзи-индикатор
        self.reagent_emoji = tk.Label(content, text="", font=('Arial', 40),
                                    bg='#2a2a2a')
        self.reagent_emoji.pack(expand=True)
        
        # Статус текстом (только "В норме" или "Критично")
        self.reagent_status = tk.Label(content, text="", font=('Arial', 11, 'bold'),
                                     bg='#2a2a2a')
        self.reagent_status.pack()
    
    def create_calibration_card(self, parent):
        header = tk.Frame(parent, bg='#f39c12', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="⚖️ CALIBRATION", font=('Arial', 9, 'bold'),
                fg='white', bg='#f39c12').pack(expand=True)
        
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Предупреждающий знак
        self.calibration_warning = tk.Label(content, text="", font=('Arial', 48),
                                          bg='#2a2a2a')
        self.calibration_warning.pack(expand=True)
        
        # Статус калибровки (только "В норме" или "Критично")
        self.calibration_status = tk.Label(content, text="", font=('Arial', 12, 'bold'),
                                         bg='#2a2a2a')
        self.calibration_status.pack()
    
    def create_supplies_card(self, parent):
        header = tk.Frame(parent, bg='#e74c3c', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="📦 SUPPLIES & WASTE", font=('Arial', 9, 'bold'),
                fg='white', bg='#e74c3c').pack(expand=True)
        
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Центральный предупреждающий знак
        warning_frame = tk.Frame(content, bg='#2a2a2a')
        warning_frame.pack(expand=True)
        
        # Большой желтый треугольник с восклицательным знаком
        self.supplies_warning = tk.Label(warning_frame, text="⚠️", font=('Arial', 48),
                                       bg='#2a2a2a', fg='#f39c12')
        self.supplies_warning.pack(expand=True)
        
        # Статус под знаком
        self.supplies_status = tk.Label(warning_frame, text="", font=('Arial', 12, 'bold'),
                                      bg='#2a2a2a')
        self.supplies_status.pack()
    
    def create_process_path_card(self, parent):
        header = tk.Frame(parent, bg='#34495e', height=30)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🔄 PROCESS PATH", font=('Arial', 9, 'bold'),
                fg='white', bg='#34495e').pack(expand=True)
        
        content = tk.Frame(parent, bg='#2a2a2a')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Красивый прогресс бар вместо визуализации пути
        self.process_progressbar = ttk.Progressbar(content, orient='horizontal', 
                                                 length=200, mode='determinate',
                                                 style='Custom.Horizontal.TProgressbar')
        self.process_progressbar.pack(expand=True, pady=15)
        
        # Настройка стиля для красивого прогресс бара
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.Horizontal.TProgressbar', 
                       thickness=20,
                       troughcolor='#34495e',
                       background='#3498db',
                       darkcolor='#3498db',
                       lightcolor='#3498db',
                       bordercolor='#2a2a2a')
        
        # Статус процесса
        self.process_status = tk.Label(content, text="", font=('Arial', 10, 'bold'),
                                     bg='#2a2a2a')
        self.process_status.pack()
        
        # Прогресс в процентах
        self.process_percentage = tk.Label(content, text="", font=('Arial', 9),
                                         fg='#cccccc', bg='#2a2a2a')
        self.process_percentage.pack(pady=2)
    
    def show_help(self):
        help_text = """
🔬 СИСТЕМА МОНИТОРИНГА ПРОЦЕССОВ - СПРАВКА

🧪 TESTS IN PROCESS (Тесты в процессе)
- Показывает количество активных тестов в реальном времени
- Статус: нормальная/высокая нагрузка

📊 QUALITY CONTROL (Контроль качества)
- График качества процессов в реальном времени
- Точность: процент успешных тестов
- Стабильность: согласованность результатов

🧴 REAGENTS STATUS (Статус реагентов)
- Индикатор состояния реагентов
- Статусы: нормально/критично

⚖️ CALIBRATION (Калибровка)
- Статус калибровки оборудования
- Время до следующей калибровки

📦 SUPPLIES & WASTE (Расходники и отходы)
- Общий статус расходных материалов и отходов
- ⚠️ - предупреждение о необходимости проверки

🔄 PROCESS PATH (Путь процесса)
- Прогресс выполнения текущего процесса
- Отображается в процентах завершения

Цветовая индикация: зеленый=норма, желтый=внимание, красный=критично
        """
        
        messagebox.showinfo("Справка по системе мониторинга", help_text)
    
    def generate_sample_data(self):
        # Случайные данные для демонстрации
        random.seed()
        
        self.sample_data = {
            'tests': random.randint(15, 25),
            'qc_quality': random.randint(85, 99),
            'reagents_status': random.choice(['good', 'critical']),
            'calibration_due': random.randint(1, 30),
            'supplies_status': random.choice(['normal', 'warning', 'critical']),
            'process_stage': random.randint(1, 5)
        }
    
    def draw_qc_graph(self, quality):
        self.qc_canvas.delete("all")
        
        width, height = 180, 80
        points = []
        
        # Генерируем случайные точки для графика
        for i in range(8):
            x = i * (width - 20) / 7 + 10
            base_y = height - 20 - (quality - 85) * 0.5
            y = base_y + random.randint(-6, 6)
            points.append((x, y))
        
        # Рисуем линию графика
        for i in range(len(points) - 1):
            self.qc_canvas.create_line(points[i][0], points[i][1], 
                                     points[i+1][0], points[i+1][1], 
                                     fill='#9b59b6', width=2, smooth=True)
        
        # Рисуем точки
        for x, y in points:
            self.qc_canvas.create_oval(x-2, y-2, x+2, y+2, fill='#9b59b6', outline='')
        
        # Линия качества
        quality_y = height - 20 - (quality - 85) * 0.5
        self.qc_canvas.create_line(10, quality_y, width-10, quality_y, 
                                 fill='#ffffff', width=1, dash=(3, 2))
    
    def update_display(self):
        data = self.sample_data
        
        # Tests in Process
        self.tests_value.config(text=str(data['tests']))
        status_text = "Нормальная нагрузка" if data['tests'] < 22 else "Высокая нагрузка"
        self.tests_status.config(text=status_text)
        
        # Quality Control
        self.draw_qc_graph(data['qc_quality'])
        self.qc_accuracy.config(text=f"Точность: {data['qc_quality']}%")
        self.qc_consistency.config(text=f"Стабильность: {random.randint(88, 96)}%")
        
        # Reagents
        if data['reagents_status'] == 'good':
            self.reagent_emoji.config(text="👍", fg='#27ae60')
            self.reagent_status.config(text="В норме", fg='#27ae60')
        else:
            self.reagent_emoji.config(text="❌", fg='#e74c3c')
            self.reagent_status.config(text="Критично", fg='#e74c3c')
        
        # Calibration
        if data['calibration_due'] > 7:
            self.calibration_warning.config(text="✅", fg='#27ae60')
            self.calibration_status.config(text="В норме", fg='#27ae60')
        else:
            self.calibration_warning.config(text="🔴", fg='#e74c3c')
            self.calibration_status.config(text="Критично", fg='#e74c3c')
        
        # Supplies & Waste
        if data['supplies_status'] == 'normal':
            self.supplies_warning.config(fg='#27ae60')
            self.supplies_status.config(text="В норме", fg='#27ae60')
        elif data['supplies_status'] == 'warning':
            self.supplies_warning.config(fg='#f39c12')
            self.supplies_status.config(text="Требует внимания", fg='#f39c12')
        else:
            self.supplies_warning.config(fg='#e74c3c')
            self.supplies_status.config(text="Критично", fg='#e74c3c')
        
        # Process Path - прогресс бар
        progress_percentage = (data['process_stage'] / 5) * 100
        self.process_progressbar['value'] = progress_percentage
        
        stages = ["Инициализация", "Подготовка", "Анализ", "Верификация", "Завершение"]
        self.process_status.config(text=stages[data['process_stage'] - 1], 
                                 fg='#27ae60' if data['process_stage'] == 5 else '#3498db')
        self.process_percentage.config(text=f"{progress_percentage:.0f}% завершено")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessMonitor(root)
    root.mainloop()