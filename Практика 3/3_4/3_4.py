import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta

class MaintenanceDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Maintenance Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1e1e1e')
        
        self.setup_ui()
        self.generate_sample_data()
        self.update_display()
    
    def setup_ui(self):
        # Заголовок
        header = tk.Frame(self.root, bg='#2d2d2d', height=80)
        header.pack(fill=tk.X, padx=20, pady=10)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🔧 ВИЗУАЛЬНЫЙ МОНИТОРИНГ ТЕХНИЧЕСКОГО ОБСЛУЖИВАНИЯ", 
                        font=('Arial', 20, 'bold'), fg='white', bg='#2d2d2d')
        title.pack(expand=True)
        
        # Периоды фильтрации
        period_frame = tk.Frame(header, bg='#2d2d2d')
        period_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(period_frame, text="Период:", font=('Arial', 11), 
                fg='white', bg='#2d2d2d').pack(side=tk.LEFT)
        
        self.period_var = tk.StringVar(value="month")
        periods = [("Неделя", "week"), ("Месяц", "month"), ("Квартал", "quarter"), ("Год", "year")]
        
        for text, value in periods:
            tk.Radiobutton(period_frame, text=text, variable=self.period_var, 
                          value=value, font=('Arial', 10), fg='white', bg='#2d2d2d',
                          selectcolor='#404040', command=self.update_display).pack(side=tk.LEFT, padx=5)
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - сводная статистика
        self.setup_stats_panel(main_container)
        
        # Правая панель - детализация
        self.setup_details_panel(main_container)
    
    def setup_stats_panel(self, parent):
        stats_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Заголовок
        stats_header = tk.Frame(stats_frame, bg='#404040', height=50)
        stats_header.pack(fill=tk.X)
        stats_header.pack_propagate(False)
        
        tk.Label(stats_header, text="📈 СТАТУС ВЫПОЛНЕНИЯ ПО ПЕРИОДАМ", 
                font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(expand=True)
        
        # Контейнер для круговых диаграмм
        charts_container = tk.Frame(stats_frame, bg='#2d2d2d')
        charts_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем 4 круговые диаграммы для разных периодов
        periods = [("ЕЖЕДНЕВНОЕ", "#3498db"), ("ЕЖЕНЕДЕЛЬНОЕ", "#e74c3c"), 
                  ("ЕЖЕМЕСЯЧНОЕ", "#f39c12"), ("КВАРТАЛЬНОЕ", "#27ae60")]
        
        self.chart_frames = []
        for i, (title, color) in enumerate(periods):
            row = i // 2
            col = i % 2
            
            chart_frame = tk.Frame(charts_container, bg='#2d2d2d')
            chart_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Заголовок диаграммы
            tk.Label(chart_frame, text=title, font=('Arial', 11, 'bold'), 
                    fg=color, bg='#2d2d2d').pack()
            
            # Холст для круговой диаграммы
            canvas = tk.Canvas(chart_frame, width=150, height=150, bg='#2d2d2d', 
                              highlightthickness=0)
            canvas.pack(pady=10)
            
            # Процент выполнения
            percent_label = tk.Label(chart_frame, text="", font=('Arial', 16, 'bold'), 
                                   fg='white', bg='#2d2d2d')
            percent_label.pack()
            
            # Статус
            status_label = tk.Label(chart_frame, text="", font=('Arial', 10), 
                                  fg='#cccccc', bg='#2d2d2d')
            status_label.pack()
            
            self.chart_frames.append({
                'canvas': canvas,
                'percent': percent_label,
                'status': status_label,
                'color': color
            })
            
            charts_container.grid_rowconfigure(row, weight=1)
            charts_container.grid_columnconfigure(col, weight=1)
    
    def setup_details_panel(self, parent):
        details_frame = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Заголовок
        details_header = tk.Frame(details_frame, bg='#404040', height=50)
        details_header.pack(fill=tk.X)
        details_header.pack_propagate(False)
        
        tk.Label(details_header, text="📋 ДЕТАЛИЗАЦИЯ ПО ОБОРУДОВАНИЮ", 
                font=('Arial', 12, 'bold'), fg='white', bg='#404040').pack(expand=True)
        
        # Холст для временной шкалы
        self.timeline_canvas = tk.Canvas(details_frame, bg='#2d2d2d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.timeline_canvas.yview)
        
        self.timeline_frame = tk.Frame(self.timeline_canvas, bg='#2d2d2d')
        self.timeline_frame.bind("<Configure>", lambda e: self.timeline_canvas.configure(
            scrollregion=self.timeline_canvas.bbox("all")))
        
        self.timeline_canvas.create_window((0, 0), window=self.timeline_frame, anchor="nw")
        self.timeline_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.timeline_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
    
    def generate_sample_data(self):
        # Генерируем случайные данные при каждом запуске
        random.seed()  # Сбрасываем seed для разных значений при каждом запуске
        
        self.equipment = [
            "Станок ЧПУ №1", "Компрессорная установка", "Транспортёрная линия",
            "Система вентиляции", "Генератор", "Пресс-форма №3",
            "Система охлаждения", "Упаковочный автомат", "Конвейер №2",
            "Насосная станция", "Электрощитовая", "Термопластавтомат"
        ]
        
        # Случайные проценты выполнения для каждого периода
        self.periods_data = {
            "daily": random.randint(70, 98),
            "weekly": random.randint(60, 95),
            "monthly": random.randint(50, 90),
            "quarterly": random.randint(40, 85)
        }
        
        # Случайные статусы для оборудования
        self.equipment_statuses = {}
        status_options = ['completed', 'pending', 'overdue', 'planned']
        
        for equipment in self.equipment:
            self.equipment_statuses[equipment] = {
                'daily': random.choice(status_options),
                'weekly': random.choice(status_options),
                'monthly': random.choice(status_options),
                'quarterly': random.choice(status_options)
            }
    
    def draw_pie_chart(self, canvas, percentage, color):
        canvas.delete("all")
        
        center_x, center_y = 75, 75
        radius = 60
        
        # Фон круга
        canvas.create_oval(center_x - radius, center_y - radius,
                          center_x + radius, center_y + radius,
                          outline='#404040', fill='#404040', width=2)
        
        # Заполненная часть
        if percentage > 0:
            angle = 360 * percentage / 100
            canvas.create_arc(center_x - radius, center_y - radius,
                            center_x + radius, center_y + radius,
                            start=90, extent=-angle, outline=color, 
                            fill=color, width=3)
        
        # Центральный круг
        canvas.create_oval(center_x - radius + 20, center_y - radius + 20,
                          center_x + radius - 20, center_y + radius - 20,
                          outline='#2d2d2d', fill='#2d2d2d', width=2)
    
    def create_timeline_item(self, parent, equipment, status_data, row):
        # Фрейм для элемента временной шкалы
        item_frame = tk.Frame(parent, bg='#404040', relief=tk.RAISED, bd=1)
        item_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Название оборудования
        tk.Label(item_frame, text=equipment, font=('Arial', 11, 'bold'), 
                fg='white', bg='#404040', width=20).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Временная шкала
        timeline_frame = tk.Frame(item_frame, bg='#404040')
        timeline_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        
        # Создаем периоды на временной шкале
        periods = [("Неделя", "daily"), ("Месяц", "weekly"), ("Квартал", "monthly"), ("Год", "quarterly")]
        
        for period_name, period_key in periods:
            period_frame = tk.Frame(timeline_frame, bg='#404040')
            period_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(period_frame, text=period_name, font=('Arial', 8), 
                    fg='#cccccc', bg='#404040').pack()
            
            # Индикатор статуса (берем из заранее сгенерированных данных)
            status = self.equipment_statuses[equipment][period_key]
            colors = {
                'completed': '#27ae60',
                'pending': '#f39c12', 
                'overdue': '#e74c3c',
                'planned': '#3498db'
            }
            
            status_canvas = tk.Canvas(period_frame, width=30, height=30, 
                                    bg='#404040', highlightthickness=0)
            status_canvas.pack(pady=2)
            
            # Рисуем индикатор
            color = colors[status]
            status_canvas.create_oval(5, 5, 25, 25, fill=color, outline=color)
            
            # Иконка статуса
            icons = {
                'completed': '✓',
                'pending': '!',
                'overdue': '×',
                'planned': '○'
            }
            status_canvas.create_text(15, 15, text=icons[status], 
                                    font=('Arial', 10, 'bold'), fill='white')
            
            # Текст статуса
            status_texts = {
                'completed': 'Выполнено',
                'pending': 'В работе', 
                'overdue': 'Просрочено',
                'planned': 'Запланировано'
            }
            tk.Label(period_frame, text=status_texts[status], font=('Arial', 7), 
                    fg=color, bg='#404040').pack()
    
    def update_display(self):
        # Обновляем круговые диаграммы
        periods = ["daily", "weekly", "monthly", "quarterly"]
        period_names = ["Ежедневное", "Еженедельное", "Ежемесячное", "Квартальное"]
        
        for i, (period, name) in enumerate(zip(periods, period_names)):
            percentage = self.periods_data[period]
            chart_data = self.chart_frames[i]
            
            self.draw_pie_chart(chart_data['canvas'], percentage, chart_data['color'])
            
            chart_data['percent'].config(text=f"{percentage}%")
            
            # Статус выполнения
            if percentage >= 90:
                status_text = "✅ ВЫПОЛНЕНО"
            elif percentage >= 70:
                status_text = "⚠️  В РАБОТЕ"
            else:
                status_text = "❌ ТРЕБУЕТ ВНИМАНИЯ"
            
            chart_data['status'].config(text=status_text)
        
        # Обновляем временную шкалу
        for widget in self.timeline_frame.winfo_children():
            widget.destroy()
        
        # Создаем элементы временной шкалы
        for i, equipment in enumerate(self.equipment):
            self.create_timeline_item(self.timeline_frame, equipment, {}, i)

if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceDashboard(root)
    root.mainloop()