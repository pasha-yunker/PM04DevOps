import tkinter as tk
from tkinter import ttk
import time
import threading

class MachineControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Панель управления машиностроительной установкой | Работа Павла Юнкер")
        self.root.geometry("700x400")  # Изначальный размер без журнала
        self.root.configure(bg='#2c3e50')
        self.root.minsize(700, 400)
        
        self.status = "offline"
        self.is_running = False
        self.log_visible = False  # Изначально журнал скрыт
        self.loading_animation = False
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="МАШИНОСТРОИТЕЛЬНАЯ УСТАНОВКА",
            font=('Arial', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        # Status panel
        self.setup_status_panel(main_frame)
        
        # Control buttons
        self.setup_control_buttons(main_frame)
        
        # Log toggle button
        self.setup_log_toggle(main_frame)
        
        # Log panel (изначально скрыта полностью)
        self.setup_log_panel(main_frame)
        
    def setup_status_panel(self, parent):
        status_frame = tk.Frame(parent, bg='#34495e', relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            status_frame,
            text="СТАТУС:",
            font=('Arial', 12, 'bold'),
            fg='#bdc3c7',
            bg='#34495e'
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="ВЫКЛЮЧЕНО",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 20), pady=10)
        
    def setup_control_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='#2c3e50')
        button_frame.pack(pady=(0, 20))
        
        # Button styles
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 14,
            'height': 2,
            'bd': 3,
            'relief': tk.RAISED
        }
        
        disabled_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 14,
            'height': 2,
            'bd': 3,
            'relief': tk.RAISED,
            'state': tk.DISABLED,
            'bg': '#95a5a6',
            'fg': '#7f8c8d'
        }
        
        self.start_btn = tk.Button(
            button_frame,
            text="ПУСК",
            bg='#27ae60',
            fg='white',
            command=self.start_machine,
            **button_style
        )
        self.start_btn.grid(row=0, column=0, padx=8, pady=5)
        
        self.resume_btn = tk.Button(
            button_frame,
            text="ВОЗОБНОВИТЬ",
            **disabled_style
        )
        self.resume_btn.grid(row=0, column=1, padx=8, pady=5)
        
        self.pause_btn = tk.Button(
            button_frame,
            text="ПАУЗА",
            **disabled_style
        )
        self.pause_btn.grid(row=0, column=2, padx=8, pady=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="СТОП",
            **disabled_style
        )
        self.stop_btn.grid(row=0, column=3, padx=8, pady=5)
        
    def setup_log_toggle(self, parent):
        toggle_frame = tk.Frame(parent, bg='#2c3e50')
        toggle_frame.pack(pady=(10, 0))
        
        self.log_toggle_btn = tk.Button(
            toggle_frame,
            text="ЖУРНАЛ СОБЫТИЙ ▼",
            font=('Arial', 10, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            relief=tk.RAISED,
            bd=2,
            command=self.toggle_log
        )
        self.log_toggle_btn.pack()
        
    def setup_log_panel(self, parent):
        # Log frame (изначально полностью скрыта - pack_forget)
        self.log_frame = tk.Frame(parent, bg='#34495e', relief=tk.SUNKEN, bd=2)
        
        # Log text area
        self.log_text = tk.Text(
            self.log_frame,
            height=8,
            bg='#2c3e50',
            fg='#ecf0f1',
            font=('Courier New', 9),
            relief=tk.FLAT,
            bd=2,
            wrap=tk.WORD
        )
        
        scrollbar = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Add initial log message
        self.add_log("Система инициализирована. Статус: ВЫКЛЮЧЕНО")
        
    def toggle_log(self):
        if self.log_visible:
            # Полностью скрываем журнал
            self.log_frame.pack_forget()
            self.log_toggle_btn.configure(text="ЖУРНАЛ СОБЫТИЙ ▼")
            self.root.geometry("700x400")
            self.log_visible = False
        else:
            # Показываем журнал
            self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            self.log_toggle_btn.configure(text="ЖУРНАЛ СОБЫТИЙ ▲")
            self.root.geometry("700x550")
            self.log_visible = True
        
    def add_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def start_loading_animation(self, base_status):
        self.loading_animation = True
        def animate():
            dots = 0
            while self.loading_animation:
                dots = (dots + 1) % 4
                loading_text = base_status + "." * dots
                self.status_label.config(text=loading_text)
                time.sleep(0.5)
            # После завершения анимации устанавливаем финальный статус
            self.update_status(self.status, self.get_status_color(self.status))
        
        threading.Thread(target=animate, daemon=True).start()
        
    def stop_loading_animation(self):
        self.loading_animation = False
        
    def get_status_color(self, status):
        colors = {
            "offline": "#e74c3c",
            "initializing": "#f39c12",
            "online": "#27ae60",
            "running": "#3498db",
            "paused": "#f39c12",
            "resuming": "#3498db",
            "stopping": "#e74c3c"
        }
        return colors.get(status, "#e74c3c")
        
    def update_status(self, new_status, color=None):
        self.status = new_status
        status_text = ""
        
        if new_status == "offline":
            status_text = "ВЫКЛЮЧЕНО"
        elif new_status == "initializing":
            status_text = "ЗАПУСК"
        elif new_status == "online":
            status_text = "ОНЛАЙН"
        elif new_status == "running":
            status_text = "РАБОТА"
        elif new_status == "paused":
            status_text = "ПАУЗА"
        elif new_status == "resuming":
            status_text = "ВОЗОБНОВЛЕНИЕ"
        elif new_status == "stopping":
            status_text = "ОСТАНОВКА"
            
        if color is None:
            color = self.get_status_color(new_status)
            
        self.status_label.config(text=status_text, fg=color)
        
    def set_button_state(self, button, state):
        if state == tk.NORMAL:
            if button == self.start_btn:
                button.config(state=state, bg='#27ae60', fg='white')
            elif button == self.resume_btn:
                button.config(state=state, bg='#3498db', fg='white', command=self.resume_machine)
            elif button == self.pause_btn:
                button.config(state=state, bg='#f39c12', fg='white', command=self.pause_machine)
            elif button == self.stop_btn:
                button.config(state=state, bg='#e74c3c', fg='white', command=self.stop_machine)
        else:
            button.config(state=state, bg='#95a5a6', fg='#7f8c8d')
        
    def start_machine(self):
        self.add_log("Запуск инициализации системы")
        self.update_status("initializing")
        self.start_loading_animation("ЗАПУСК")
        
        # Disable buttons
        self.set_button_state(self.start_btn, tk.DISABLED)
        self.set_button_state(self.resume_btn, tk.DISABLED)
        self.set_button_state(self.pause_btn, tk.DISABLED)
        self.set_button_state(self.stop_btn, tk.DISABLED)
        
        # Simulate initialization
        self.root.after(1000, lambda: self.add_log("Проверка системных компонентов"))
        self.root.after(2000, lambda: self.add_log("Инициализация двигателей"))
        self.root.after(3000, lambda: self.add_log("Система готова к работе"))
        
        self.root.after(3000, self.finish_start)
        
    def finish_start(self):
        self.stop_loading_animation()
        self.update_status("online")
        self.set_button_state(self.pause_btn, tk.NORMAL)
        self.set_button_state(self.stop_btn, tk.NORMAL)
        self.is_running = False
        
    def resume_machine(self):
        self.add_log("Возобновление работы системы")
        self.update_status("resuming")
        self.start_loading_animation("ВОЗОБНОВЛЕНИЕ")
        
        # Disable buttons
        self.set_button_state(self.resume_btn, tk.DISABLED)
        self.set_button_state(self.pause_btn, tk.DISABLED)
        self.set_button_state(self.stop_btn, tk.DISABLED)
        
        # Simulate resuming
        self.root.after(1000, lambda: self.add_log("Перезапуск системных процессов"))
        self.root.after(2000, lambda: self.add_log("Система возобновила работу"))
        
        self.root.after(2000, self.finish_resume)
        
    def finish_resume(self):
        self.stop_loading_animation()
        self.update_status("online")
        self.set_button_state(self.pause_btn, tk.NORMAL)
        self.set_button_state(self.stop_btn, tk.NORMAL)
        self.is_running = False
        
    def pause_machine(self):
        self.add_log("Пауза выполнения")
        self.update_status("paused")
        self.set_button_state(self.resume_btn, tk.NORMAL)
        self.set_button_state(self.pause_btn, tk.DISABLED)
        self.set_button_state(self.stop_btn, tk.NORMAL)
        self.is_running = False
        
    def stop_machine(self):
        self.add_log("Остановка системы")
        self.update_status("stopping")
        self.start_loading_animation("ОСТАНОВКА")
        
        # Disable buttons
        self.set_button_state(self.resume_btn, tk.DISABLED)
        self.set_button_state(self.pause_btn, tk.DISABLED)
        self.set_button_state(self.stop_btn, tk.DISABLED)
        
        # Simulate stop
        self.root.after(1000, lambda: self.add_log("Завершение процессов"))
        self.root.after(2000, lambda: self.add_log("Система остановлена"))
        
        self.root.after(2000, self.finish_stop)
        
    def finish_stop(self):
        self.stop_loading_animation()
        self.update_status("offline")
        self.set_button_state(self.start_btn, tk.NORMAL)
        self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = MachineControlPanel(root)
    root.mainloop()