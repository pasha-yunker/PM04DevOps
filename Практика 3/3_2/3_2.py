import tkinter as tk
from tkinter import ttk
from datetime import datetime

class AdvancedLaboratorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная система анализа")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')

        try:
            self.root.state('zoomed')
        except Exception:
            pass

        # партии
        self.batches = [
            {'id': 1, 'name': 'Партия A', 'status': 'queued', 'progress': 100, 'samples': 20},
            {'id': 2, 'name': 'Партия B', 'status': 'queued', 'progress': 65, 'samples': 15},
            {'id': 3, 'name': 'Партия C', 'status': 'queued', 'progress': 0, 'samples': 25},
            {'id': 4, 'name': 'Партия D', 'status': 'queued', 'progress': 30, 'samples': 18}
        ]

        self.system_status = "stopped"
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Заголовок
        title_label = tk.Label(header_frame,
                 text="ЛАБОРАТОРНАЯ СИСТЕМА АНАЛИЗА ОБРАЗЦОВ",
                 font=('Arial', 24, 'bold'),
                 fg='#ffffff',
                 bg='#2c3e50')
        title_label.pack(pady=20)

        # Кнопки в правом верхнем углу
        top_buttons_frame = tk.Frame(header_frame, bg='#2c3e50')
        top_buttons_frame.place(relx=0.98, rely=0.5, anchor='e')

        # Кнопка справки
        help_btn = tk.Button(top_buttons_frame, text="📖", font=('Arial', 16),
                           bg='#3498db', fg='white', width=3, height=1,
                           command=self.show_help)
        help_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Кнопка настроек
        settings_btn = tk.Button(top_buttons_frame, text="⚙", font=('Arial', 16),
                               bg='#95a5a6', fg='white', width=3, height=1,
                               command=self.show_settings)
        settings_btn.pack(side=tk.RIGHT)

        # content
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # left panel - сильно сужена
        left_frame = tk.Frame(content_frame, bg='#ffffff', width=350, relief=tk.RAISED, bd=1)  # Сузили до 350
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_frame.pack_propagate(False)
        self.setup_batch_overview(left_frame)

        # center panel - без изменений
        center_frame = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        self.setup_main_indicators(center_frame)

        # right panel - сильно расширен
        right_frame = tk.Frame(content_frame, bg='#ffffff', width=750, relief=tk.RAISED, bd=1)  # Расширили до 750
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        self.setup_expanded_event_log(right_frame)

    # ==== партии ====
    def setup_batch_overview(self, parent):
        header = tk.Frame(parent, bg='#34495e', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="ПАРТИИ ОБРАЗЦОВ",
                 font=('Arial', 14, 'bold'),
                 fg='white', bg='#34495e').pack(pady=15)

        container = tk.Frame(parent, bg='#ffffff')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')

        scrollable_frame.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for batch in self.batches:
            self.create_batch_card(scrollable_frame, batch)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_batch_card(self, parent, batch):
        card_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1, padx=10, pady=8)  # Уменьшены отступы
        card_frame.pack(fill=tk.X, pady=3)  # Уменьшен промежуток между карточками

        # Верхняя строка - название партии и кнопка
        top_row = tk.Frame(card_frame, bg='#f8f9fa')
        top_row.pack(fill=tk.X)

        # Название партии
        tk.Label(top_row, text=batch['name'],
                 font=('Arial', 11, 'bold'),  # Уменьшен шрифт
                 bg='#f8f9fa', fg='#2c3e50').pack(side=tk.LEFT, anchor='w')

        # Кнопка управления партией
        btn = tk.Button(top_row, font=('Arial', 9, 'bold'), width=8)  # Уменьшена кнопка
        btn.pack(side=tk.RIGHT)

        btn.config(text="Запуск", bg='#27ae60', fg='white',
                   command=lambda b=batch, w=btn: self.start_batch(b, w))

        # Информация об образцах
        samples_frame = tk.Frame(card_frame, bg='#f8f9fa')
        samples_frame.pack(fill=tk.X, pady=(3, 0))  # Уменьшен отступ

        tk.Label(samples_frame, text=f"Образцы: {batch['samples']} шт.",
                 font=('Arial', 9),  # Уменьшен шрифт
                 bg='#f8f9fa', fg='#7f8c8d').pack(side=tk.LEFT)

        # Прогресс-бар
        progress_frame = tk.Frame(card_frame, bg='#f8f9fa')
        progress_frame.pack(fill=tk.X, pady=(3, 0))  # Уменьшен отступ

        # Прогресс-бар компактный
        progress_bar = ttk.Progressbar(progress_frame, value=batch['progress'], length=200)  # Укорочен прогресс-бар
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # Процент выполнения
        tk.Label(progress_frame, text=f"{batch['progress']}%",
                 font=('Arial', 9, 'bold'),  # Уменьшен шрифт
                 bg='#f8f9fa', fg='#2c3e50').pack(side=tk.RIGHT)

    # ==== центр ====
    def setup_main_indicators(self, parent):
        status_frame = tk.Frame(parent, bg='#ecf0f1', height=120)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(status_frame,
                                     text="СИСТЕМА ОСТАНОВЛЕНА",
                                     font=('Arial', 18, 'bold'),
                                     fg='#e74c3c', bg='#ecf0f1')
        self.status_label.pack(pady=40)

        control_frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=10)
        control_frame.pack(fill=tk.X)
        self.setup_control_buttons(control_frame)

    def setup_control_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg='#ffffff')
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="▶ ЗАПУСК СИСТЕМЫ",
                                   font=('Arial', 11, 'bold'),
                                   bg='#27ae60', fg='white',
                                   height=2, width=18,
                                   command=self.start_system)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(btn_frame, text="⏸ ПАУЗА",
                                   font=('Arial', 12, 'bold'),
                                   bg='#95a5a6', fg='white',
                                   height=2, width=12,
                                   command=self.pause_system,
                                   state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="⏹ ОСТАНОВИТЬ",
                                  font=('Arial', 12, 'bold'),
                                  bg='#95a5a6', fg='white',
                                  height=2, width=15,
                                  command=self.stop_system,
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # шире кнопка аварийной остановки
        self.emergency_btn = tk.Button(btn_frame, text="🚨 АВАРИЙНАЯ ОСТАНОВКА",
                                       font=('Arial', 12, 'bold'),
                                       bg='#95a5a6', fg='white',
                                       height=2, width=25,
                                       command=self.emergency_stop,
                                       state=tk.DISABLED)
        self.emergency_btn.pack(side=tk.LEFT, padx=5)

    # ==== журнал ====
    def setup_expanded_event_log(self, parent):
        header = tk.Frame(parent, bg='#34495e', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Заголовок журнала
        log_header_frame = tk.Frame(header, bg='#34495e')
        log_header_frame.pack(expand=True)
        
        tk.Label(log_header_frame, text="ЖУРНАЛ СОБЫТИЙ",
                 font=('Arial', 14, 'bold'),
                 fg='white', bg='#34495e').pack(pady=15)

        log_frame = tk.Frame(parent, bg='#ffffff')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, height=30, bg='#2c3e50', fg='white',
                                font=('Consolas', 10), relief=tk.FLAT, bd=0)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_log("Система инициализирована. Готова к работе.", "info")

    # ==== лог ====
    def add_log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    # ==== настройки ====
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки системы")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#f8f9fa')
        settings_window.transient(self.root)
        settings_window.grab_set()

        tk.Label(settings_window, text="НАСТРОЙКИ СИСТЕМЫ", 
                 font=('Arial', 16, 'bold'), bg='#f8f9fa').pack(pady=20)

        # Настройки звука
        sound_frame = tk.Frame(settings_window, bg='#f8f9fa', padx=20)
        sound_frame.pack(fill=tk.X, pady=10)
        
        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(sound_frame, text="Звуковые уведомления", 
                      variable=self.sound_var, font=('Arial', 12), 
                      bg='#f8f9fa').pack(anchor='w')

        # Настройки автосохранения
        auto_frame = tk.Frame(settings_window, bg='#f8f9fa', padx=20)
        auto_frame.pack(fill=tk.X, pady=10)
        
        self.auto_save_var = tk.BooleanVar(value=True)
        tk.Checkbutton(auto_frame, text="Автосохранение каждые 5 минут", 
                      variable=self.auto_save_var, font=('Arial', 12), 
                      bg='#f8f9fa').pack(anchor='w')

        # Кнопка закрытия
        tk.Button(settings_window, text="Закрыть", font=('Arial', 12),
                 bg='#95a5a6', fg='white', command=settings_window.destroy).pack(pady=20)

    # ==== справка ====
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Справочник системы")
        help_window.geometry("500x500")
        help_window.configure(bg='#f8f9fa')
        help_window.transient(self.root)
        help_window.grab_set()

        tk.Label(help_window, text="СПРАВОЧНИК СИСТЕМЫ", 
                 font=('Arial', 16, 'bold'), bg='#f8f9fa').pack(pady=20)

        help_text = """
        УПРАВЛЕНИЕ СИСТЕМОЙ:

        ▶ ЗАПУСК СИСТЕМЫ - Запуск анализа всех партий
        ⏸ ПАУЗА - Временная остановка процессов
        ⏹ ОСТАНОВИТЬ - Полная остановка системы
        🚨 АВАРИЙНАЯ ОСТАНОВКА - Немедленный стоп

        ЦВЕТОВАЯ ИНДИКАЦИЯ СТАТУСА СИСТЕМЫ:

        🟢 ЗЕЛЕНЫЙ - "СИСТЕМА РАБОТАЕТ"
        Система функционирует в нормальном режиме

        🟠 ОРАНЖЕВЫЙ - "СИСТЕМА НА ПАУЗЕ"
        Процессы временно приостановлены

        🔴 КРАСНЫЙ - "СИСТЕМА ОСТАНОВЛЕНА"
        Система полностью остановлена

        🚨 ТЕМНО-КРАСНЫЙ - "АВАРИЙНАЯ ОСТАНОВКА!"
        Экстренная остановка системы

        УПРАВЛЕНИЕ ПАРТИЯМИ:

        • Запуск/остановка отдельных партий
        • Мониторинг прогресса выполнения
        • Отслеживание количества образцов

        ЖУРНАЛ СОБЫТИЙ:

        • История всех операций
        • Временные метки событий
        • Отслеживание статусов системы
        """

        text_widget = tk.Text(help_window, wrap=tk.WORD, font=('Arial', 11),
                            bg='#ffffff', fg='#2c3e50', padx=20, pady=20)
        text_widget.insert('1.0', help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20)

        tk.Button(help_window, text="Закрыть", font=('Arial', 12),
                 bg='#3498db', fg='white', command=help_window.destroy).pack(pady=10)

    # ==== система ====
    def start_system(self):
        self.system_status = "running"
        self.status_label.config(text="СИСТЕМА РАБОТАЕТ", fg='#27ae60')
        self.start_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.pause_btn.config(state=tk.NORMAL, bg='#f39c12')
        self.stop_btn.config(state=tk.NORMAL, bg='#e74c3c')
        self.emergency_btn.config(state=tk.NORMAL, bg='#c0392b')
        self.add_log("Система запущена", "success")

    def pause_system(self):
        self.system_status = "paused"
        self.status_label.config(text="СИСТЕМА НА ПАУЗЕ", fg='#f39c12')
        self.start_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.stop_btn.config(state=tk.NORMAL, bg='#e74c3c')
        self.emergency_btn.config(state=tk.NORMAL, bg='#c0392b')
        self.add_log("Система поставлена на паузу", "warning")

    def stop_system(self):
        self.system_status = "stopped"
        self.status_label.config(text="СИСТЕМА ОСТАНОВЛЕНА", fg='#e74c3c')
        self.start_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.stop_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.emergency_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.add_log("Система остановлена", "warning")

    def emergency_stop(self):
        self.system_status = "emergency"
        self.status_label.config(text="АВАРИЙНАЯ ОСТАНОВКА!", fg='#c0392b')
        self.start_btn.config(state=tk.NORMAL, bg='#27ae60')
        self.pause_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.stop_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.emergency_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.add_log("Выполнена аварийная остановка системы!", "error")

    # ==== партии ====
    def start_batch(self, batch, button):
        batch['status'] = 'processing'
        button.config(text="Стоп", bg='#e74c3c',
                      command=lambda b=batch, w=button: self.stop_batch(b, w))
        self.add_log(f"Запущена {batch['name']}", "success")

    def stop_batch(self, batch, button):
        batch['status'] = 'queued'
        button.config(text="Запуск", bg='#27ae60',
                      command=lambda b=batch, w=button: self.start_batch(b, w))
        self.add_log(f"Остановлена {batch['name']}", "warning")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedLaboratorySystem(root)
    root.mainloop()