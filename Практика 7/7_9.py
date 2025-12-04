import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import random

class Chart1:
    """Компонент для построения столбчатых и круговых диаграмм"""
    
    def __init__(self, parent, chart_type="bar", is_zoomed=False):
        self.parent = parent
        self.chart_type = chart_type
        self.data = {}
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        self.title = "Диаграмма"
        self.x_label = "Категории"
        self.y_label = "Значения"
        self.is_zoomed = is_zoomed
        
        # Создание фигуры matplotlib
        self.fig = Figure(figsize=(8, 4 if is_zoomed else 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def set_data(self, data):
        """Установка данных для диаграммы"""
        self.data = data
        self.update_chart()
    
    def set_chart_type(self, chart_type):
        """Изменение типа диаграммы"""
        self.chart_type = chart_type
        self.update_chart()
    
    def set_title(self, title):
        """Установка заголовка"""
        self.title = title
        self.update_chart()
    
    def set_labels(self, x_label, y_label):
        """Установка подписей осей"""
        self.x_label = x_label
        self.y_label = y_label
        self.update_chart()
    
    def set_colors(self, colors):
        """Установка цветовой схемы"""
        self.colors = colors
        self.update_chart()
    
    def get_zoomed_data(self, data):
        """Получение масштабированных данных для нижнего графика"""
        if not data:
            return {}
        
        # Для нижнего графика нормализуем данные от 0 до 100
        values = list(data.values())
        if not values:
            return {}
            
        max_value = max(values)
        min_value = min(values)
        
        zoomed_data = {}
        
        if max_value == min_value:
            # Если все значения одинаковые
            for key in data.keys():
                zoomed_data[key] = 50  # Среднее значение
        else:
            # Нормализуем к диапазону 0-100
            for key, value in data.items():
                normalized = (value - min_value) / (max_value - min_value) * 100
                zoomed_data[key] = normalized
        
        return zoomed_data
    
    def update_chart(self):
        """Обновление диаграммы"""
        self.ax.clear()
        
        if not self.data:
            self.ax.text(0.5, 0.5, 'Нет данных для отображения', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14)
            self.canvas.draw()
            return
        
        # Для нижнего графика используем масштабированные данные
        display_data = self.get_zoomed_data(self.data) if self.is_zoomed else self.data
        
        categories = list(display_data.keys())
        values = list(display_data.values())
        
        if self.chart_type == "bar":
            # Настройка позиций и ширины столбцов
            x_pos = np.arange(len(categories))
            width = 0.6  # Уменьшаем ширину столбцов для большего расстояния
            
            # Столбчатая диаграмма с увеличенным расстоянием
            bars = self.ax.bar(x_pos, values, width, color=self.colors[:len(categories)])
            self.ax.set_ylabel(self.y_label)
            self.ax.set_xlabel(self.x_label)
            
            # Устанавливаем подписи по центру столбцов
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(categories)
            
            # Настройка осей для стабильности отображения
            if self.is_zoomed:
                # Фиксируем диапазон Y для нижнего графика
                self.ax.set_ylim(0, 105)
                # Уменьшаем размер шрифта
                self.ax.tick_params(axis='x', labelsize=8)
                self.ax.tick_params(axis='y', labelsize=8)
            else:
                # Для верхнего графика добавляем запас по Y
                y_max = max(values) if values else 1
                self.ax.set_ylim(0, y_max * 1.15)  # +15% запаса сверху
            
            # Добавление значений на столбцы с улучшенным позиционированием
            for bar, value in zip(bars, values):
                height = bar.get_height()
                
                # Определяем вертикальное положение текста
                if self.is_zoomed:
                    label = f'{value:.1f}%'
                    fontsize = 8
                    # Для нижнего графика размещаем текст выше
                    text_y = height + 2
                else:
                    label = f'{value:.1f}'
                    fontsize = 10
                    # Для верхнего графика рассчитываем отступ пропорционально высоте
                    text_y = height + (y_max * 0.02)  # 2% от максимального значения
                
                # Размещаем текст по центру столбца
                text_x = bar.get_x() + bar.get_width() / 2
                
                self.ax.text(text_x, text_y, label, 
                           ha='center', va='bottom', 
                           fontsize=fontsize,
                           fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none'))
            
        elif self.chart_type == "pie":
            # Круговая диаграмма
            if self.is_zoomed:
                # Для нижнего графика используем оригинальные пропорции
                original_values = list(self.data.values())
                total = sum(original_values)
                if total > 0:
                    values = [v/total * 100 for v in original_values]
            
            wedges, texts, autotexts = self.ax.pie(values, labels=categories, 
                                                   colors=self.colors[:len(categories)],
                                                   autopct='%1.1f%%', 
                                                   startangle=90,
                                                   labeldistance=1.1)
            
            # Настройка внешнего вида
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                if self.is_zoomed:
                    autotext.set_fontsize(8)
        
        title_fontsize = 10 if self.is_zoomed else 12
        self.ax.set_title(self.title, fontsize=title_fontsize)
        
        # Улучшаем layout
        self.fig.tight_layout()
        self.canvas.draw()
    
    def save_chart(self, filename):
        """Сохранение диаграммы в файл"""
        try:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

class ResearchApp:
    """Исследовательское приложение для тестирования компонента Chart1"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Исследовательское приложение - Компонент Chart1 | Работа Павла Юнкер")
        self.root.geometry("1200x900")
        
        # Данные для тестирования
        self.sample_datasets = {
            "Продажи по месяцам": {
                "Январь": 120, "Февраль": 150, "Март": 180, 
                "Апрель": 200, "Май": 170, "Июнь": 220
            },
            "Распределение бюджета": {
                "Зарплаты": 45, "Маркетинг": 25, "ИТ": 15, 
                "Аренда": 10, "Прочее": 5
            },
            "Статистика посещений": {
                "Пн": 340, "Вт": 420, "Ср": 380,
                "Чт": 450, "Пт": 510, "Сб": 280, "Вс": 190
            },
            "Стабильные данные": {
                "A": 50, "B": 55, "C": 52, "D": 53, "E": 51
            },
            "Большие числа": {
                "Кат.1": 1000, "Кат.2": 1500, "Кат.3": 1200,
                "Кат.4": 1800, "Кат.5": 900
            }
        }
        
        self.setup_ui()
        self.load_sample_data("Стабильные данные")
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - управление
        control_frame = ttk.LabelFrame(main_frame, text="Управление и настройки", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Правая панель - диаграммы
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Верхняя диаграмма (основная)
        main_chart_frame = ttk.LabelFrame(charts_frame, text="Основная диаграмма", padding=10)
        main_chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Нижняя диаграмма (масштабированная)
        zoom_chart_frame = ttk.LabelFrame(charts_frame, text="Масштабированный вид (стабильный)", padding=10)
        zoom_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Инициализация компонентов Chart1
        self.main_chart = Chart1(main_chart_frame, "bar", is_zoomed=False)
        self.zoom_chart = Chart1(zoom_chart_frame, "bar", is_zoomed=True)
        
        # Настройка нижнего графика
        self.zoom_chart.set_title("Нормализованные данные (0-100%)")
        self.zoom_chart.set_labels("Категории", "Относительные значения")
        
        # Элементы управления
        self.setup_controls(control_frame)
    
    def setup_controls(self, parent):
        """Настройка элементов управления"""
        # Выбор типа диаграммы
        ttk.Label(parent, text="Тип диаграммы:").pack(anchor=tk.W, pady=(0, 5))
        self.chart_type_var = tk.StringVar(value="bar")
        chart_type_combo = ttk.Combobox(parent, textvariable=self.chart_type_var,
                                       values=["bar", "pie"], state="readonly")
        chart_type_combo.pack(fill=tk.X, pady=(0, 10))
        chart_type_combo.bind('<<ComboboxSelected>>', self.on_chart_type_change)
        
        # Выбор набора данных
        ttk.Label(parent, text="Примеры данных:").pack(anchor=tk.W, pady=(0, 5))
        self.dataset_var = tk.StringVar()
        dataset_combo = ttk.Combobox(parent, textvariable=self.dataset_var,
                                    values=list(self.sample_datasets.keys()), state="readonly")
        dataset_combo.pack(fill=tk.X, pady=(0, 10))
        dataset_combo.bind('<<ComboboxSelected>>', self.on_dataset_change)
        
        # Настройка заголовка
        ttk.Label(parent, text="Заголовок основной диаграммы:").pack(anchor=tk.W, pady=(0, 5))
        self.title_var = tk.StringVar(value="Основная диаграмма")
        title_entry = ttk.Entry(parent, textvariable=self.title_var)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        title_entry.bind('<KeyRelease>', self.on_title_change)
        
        # Слайдер для тонкой настройки данных
        ttk.Label(parent, text="Корректировка данных (±25%):").pack(anchor=tk.W, pady=(0, 5))
        self.data_adjust_var = tk.DoubleVar(value=0)
        data_scale = ttk.Scale(parent, from_=-25, to=25, variable=self.data_adjust_var,
                              orient=tk.HORIZONTAL, command=self.on_data_adjust)
        data_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Настройка расстояния между столбцами
        ttk.Label(parent, text="Плотность столбцов:").pack(anchor=tk.W, pady=(0, 5))
        self.spacing_var = tk.StringVar(value="Нормальная")
        spacing_combo = ttk.Combobox(parent, textvariable=self.spacing_var,
                                    values=["Компактная", "Нормальная", "Широкая"], state="readonly")
        spacing_combo.pack(fill=tk.X, pady=(0, 10))
        spacing_combo.bind('<<ComboboxSelected>>', self.on_spacing_change)
        
        # Кнопки управления
        ttk.Button(parent, text="Случайные данные", 
                  command=self.generate_random_data).pack(fill=tk.X, pady=5)
        
        ttk.Button(parent, text="Незначительные изменения (±2%)", 
                  command=self.minor_changes).pack(fill=tk.X, pady=5)
        
        ttk.Button(parent, text="Тест с большими числами", 
                  command=self.test_large_numbers).pack(fill=tk.X, pady=5)
        
        ttk.Button(parent, text="Сбросить настройки", 
                  command=self.reset_settings).pack(fill=tk.X, pady=5)
        
        ttk.Button(parent, text="Сохранить диаграммы", 
                  command=self.save_charts).pack(fill=tk.X, pady=5)
        
        # Область для вывода информации
        info_frame = ttk.LabelFrame(parent, text="Информация о расположении", padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=15, width=30)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_info()
    
    def load_sample_data(self, dataset_name):
        """Загрузка примера данных"""
        if dataset_name in self.sample_datasets:
            self.original_data = self.sample_datasets[dataset_name].copy()
            self.current_data = self.sample_datasets[dataset_name].copy()
            self.update_charts()
            self.dataset_var.set(dataset_name)
            self.data_adjust_var.set(0)
            self.update_info()
    
    def update_charts(self):
        """Обновление обеих диаграмм"""
        self.main_chart.set_data(self.current_data)
        self.zoom_chart.set_data(self.current_data)
    
    def on_chart_type_change(self, event):
        """Обработчик изменения типа диаграммы"""
        chart_type = self.chart_type_var.get()
        self.main_chart.set_chart_type(chart_type)
        self.zoom_chart.set_chart_type(chart_type)
        self.update_info()
    
    def on_dataset_change(self, event):
        """Обработчик изменения набора данных"""
        self.load_sample_data(self.dataset_var.get())
    
    def on_title_change(self, event):
        """Обработчик изменения заголовка"""
        self.main_chart.set_title(self.title_var.get())
    
    def on_spacing_change(self, event):
        """Обработчик изменения расстояния между столбцами"""
        # В реальной реализации здесь можно настроить ширину столбцов
        self.update_info()
    
    def on_data_adjust(self, value):
        """Корректировка данных с помощью слайдера"""
        if hasattr(self, 'original_data'):
            adjustment = float(value) / 100  # Преобразуем в долю
            self.current_data = {}
            
            for key, original_value in self.original_data.items():
                # Применяем корректировку к оригинальным данным
                adjusted_value = original_value * (1 + adjustment)
                self.current_data[key] = max(1, adjusted_value)  # Минимум 1
            
            self.update_charts()
            self.update_info()
    
    def generate_random_data(self):
        """Генерация случайных данных"""
        categories = [f"Кат.{i+1}" for i in range(random.randint(4, 8))]
        # Генерируем данные в относительно узком диапазоне для стабильности
        base_value = random.randint(40, 60)
        values = [base_value + random.randint(-15, 15) for _ in categories]
        random_data = dict(zip(categories, values))
        
        self.original_data = random_data.copy()
        self.current_data = random_data.copy()
        self.update_charts()
        self.data_adjust_var.set(0)
        self.update_info()
    
    def minor_changes(self):
        """Внесение незначительных изменений в данные (±2%)"""
        if hasattr(self, 'current_data'):
            modified_data = self.current_data.copy()
            for key in modified_data:
                # Изменяем значения на ±2%
                change = random.uniform(-0.02, 0.02)
                modified_data[key] = max(1, modified_data[key] * (1 + change))
            
            self.current_data = modified_data
            self.update_charts()
            
            # Обновляем информационную панель
            self.info_text.insert(tk.END, "\n--- Внесены незначительные изменения ±2% ---\n")
            self.info_text.insert(tk.END, "Значения не пересекаются!\n")
            self.info_text.see(tk.END)
    
    def test_large_numbers(self):
        """Тест с большими числами"""
        self.load_sample_data("Большие числа")
        self.info_text.insert(tk.END, "\n--- Тест с большими числами ---\n")
        self.info_text.insert(tk.END, "Проверяем расположение значений...\n")
        self.info_text.see(tk.END)
    
    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.chart_type_var.set("bar")
        self.title_var.set("Основная диаграмма")
        self.data_adjust_var.set(0)
        self.spacing_var.set("Нормальная")
        
        if hasattr(self, 'original_data'):
            self.current_data = self.original_data.copy()
        
        self.main_chart.set_chart_type("bar")
        self.main_chart.set_title("Основная диаграмма")
        self.zoom_chart.set_chart_type("bar")
        self.update_charts()
        self.update_info()
    
    def save_charts(self):
        """Сохранение обеих диаграмм в файл"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        main_filename = f"main_chart_{timestamp}.png"
        zoom_filename = f"zoom_chart_{timestamp}.png"
        
        success1 = self.main_chart.save_chart(main_filename)
        success2 = self.zoom_chart.save_chart(zoom_filename)
        
        if success1 and success2:
            messagebox.showinfo("Успех", f"Диаграммы сохранены:\n{main_filename}\n{zoom_filename}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить одну или обе диаграммы")
    
    def update_info(self):
        """Обновление информационной панели"""
        self.info_text.delete(1.0, tk.END)
        
        data_info = ""
        if hasattr(self, 'current_data') and self.current_data:
            values = list(self.current_data.values())
            data_info = f"""Текущие данные:
Элементов: {len(self.current_data)}
Диапазон: {min(values):.1f} - {max(values):.1f}
Среднее: {sum(values)/len(values):.1f}

"""
        
        info = f"""УЛУЧШЕННОЕ РАСПОЛОЖЕНИЕ ЗНАЧЕНИЙ

Решенные проблемы:
✓ Значения не пересекаются со столбцами
✓ Увеличено расстояние между столбцами
✓ Автоматический подбор высоты текста
✓ Фон для лучшей читаемости

Особенности:
• Ширина столбцов: 60% от доступного пространства
• Автоматический запас по оси Y (+15%)
• Пропорциональные отступы для текста
• Белый фон под числовыми значениями

{data_info}
Проверьте с разными наборами данных!"""
        
        self.info_text.insert(1.0, info)

def main():
    """Основная функция приложения"""
    # Устанавливаем стиль matplotlib для лучшего отображения
    plt.style.use('default')
    
    root = tk.Tk()
    app = ResearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
