import tkinter as tk
from tkinter import ttk, messagebox
import random

class ByteSwitchApp:
    def __init__(self, root):
        """
        Инициализация главного окна приложения
        """
        # Сохраняем ссылку на главное окно
        self.root = root
        # Устанавливаем заголовок окна
        self.root.title("Генератор случайных 4 байт - Визуализация переключателей")
        # Устанавливаем размер окна
        self.root.geometry("900x650")  # Увеличили окно для новых данных
        # Разрешаем изменение размера окна для удобства
        self.root.resizable(True, True)
        
        # Создаем переменные для хранения значений байтов
        self.byte_vars = [tk.StringVar() for _ in range(4)]
        # Создаем переменные для хранения двоичных представлений
        self.binary_vars = [tk.StringVar() for _ in range(4)]
        # СОЗДАЕМ ПЕРЕМЕННЫЕ ДЛЯ ХРАНЕНИЯ 16-РИЧНЫХ ПРЕДСТАВЛЕНИЙ
        self.hex_vars = [tk.StringVar() for _ in range(4)]
        
        # Инициализируем приложение
        self.setup_ui()
        # Генерируем первые случайные байты
        self.generate_bytes()
    
    def setup_ui(self):
        """
        Создание и размещение всех элементов интерфейса
        """
        # Основной контейнер с отступами
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === ЗАГОЛОВОК ПРИЛОЖЕНИЯ ===
        title_label = ttk.Label(
            main_frame, 
            text="ГЕНЕРАТОР СЛУЧАЙНЫХ 4 БАЙТ", 
            font=("Arial", 16, "bold"),
            foreground="darkblue"
        )
        title_label.pack(pady=(0, 20))
        
        # === ОПИСАНИЕ ПРИЛОЖЕНИЯ ===
        description_text = (
            "Программа генерирует 4 случайных байта (32 бита) \n"
            "и визуализирует их как физические переключатели\n"
            "● = ВКЛЮЧЕН (1)    ○ = ВЫКЛЮЧЕН (0)"
        )
        desc_label = ttk.Label(
            main_frame, 
            text=description_text,
            font=("Arial", 10),
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))
        
        # === ФРЕЙМ ДЛЯ КНОПОК УПРАВЛЕНИЯ ===
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(0, 20))
        
        # Кнопка генерации новых байт
        generate_btn = ttk.Button(
            button_frame,
            text="Сгенерировать новые байты",
            command=self.generate_bytes
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка выхода из приложения
        exit_btn = ttk.Button(
            button_frame,
            text="Выход",
            command=self.root.quit
        )
        exit_btn.pack(side=tk.LEFT)
        
        # === ФРЕЙМ ДЛЯ ОТОБРАЖЕНИЯ БАЙТОВ В РАЗЛИЧНЫХ ФОРМАТАХ ===
        bytes_display_frame = ttk.LabelFrame(
            main_frame, 
            text="ПРЕДСТАВЛЕНИЕ БАЙТОВ В РАЗЛИЧНЫХ ФОРМАТАХ",
            padding="10"
        )
        bytes_display_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Создаем метки для отображения байтов в десятичном, двоичном и 16-ричном формате
        for i in range(4):
            byte_frame = ttk.Frame(bytes_display_frame)
            byte_frame.pack(fill=tk.X, pady=5)
            
            # Метка с номером байта
            byte_label = ttk.Label(
                byte_frame, 
                text=f"Байт {i+1}:", 
                width=8,
                font=("Arial", 10, "bold")
            )
            byte_label.pack(side=tk.LEFT)
            
            # Метка с десятичным представлением
            decimal_label = ttk.Label(
                byte_frame,
                textvariable=self.byte_vars[i],
                width=15,
                font=("Arial", 9),
                foreground="darkgreen"
            )
            decimal_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Метка с двоичным представлением
            binary_label = ttk.Label(
                byte_frame,
                textvariable=self.binary_vars[i],
                font=("Courier New", 9, "bold"),
                foreground="darkred",
                width=20
            )
            binary_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # МЕТКА С 16-РИЧНЫМ ПРЕДСТАВЛЕНИЕМ
            hex_label = ttk.Label(
                byte_frame,
                textvariable=self.hex_vars[i],
                font=("Courier New", 9, "bold"),
                foreground="darkblue",
                width=15
            )
            hex_label.pack(side=tk.LEFT)
        
        # === ФРЕЙМ ДЛЯ СВОДНОЙ ИНФОРМАЦИИ ===
        summary_frame = ttk.LabelFrame(
            main_frame,
            text="СВОДНАЯ ИНФОРМАЦИЯ О ВСЕХ 4 БАЙТАХ",
            padding="10"
        )
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Создаем переменные для сводной информации
        self.summary_decimal = tk.StringVar()
        self.summary_binary = tk.StringVar()
        self.summary_hex = tk.StringVar()
        
        # Отображаем сводную информацию в три строки для лучшей читаемости
        # Десятичное представление
        decimal_frame = ttk.Frame(summary_frame)
        decimal_frame.pack(fill=tk.X, pady=2)
        ttk.Label(decimal_frame, text="Десятичное:", width=12).pack(side=tk.LEFT)
        ttk.Label(decimal_frame, textvariable=self.summary_decimal, font=("Arial", 9, "bold"), foreground="darkgreen").pack(side=tk.LEFT)
        
        # Двоичное представление
        binary_frame = ttk.Frame(summary_frame)
        binary_frame.pack(fill=tk.X, pady=2)
        ttk.Label(binary_frame, text="Двоичное:", width=12).pack(side=tk.LEFT)
        ttk.Label(binary_frame, textvariable=self.summary_binary, font=("Courier New", 9, "bold"), foreground="darkred").pack(side=tk.LEFT)
        
        # 16-ричное представление
        hex_frame = ttk.Frame(summary_frame)
        hex_frame.pack(fill=tk.X, pady=2)
        ttk.Label(hex_frame, text="16-ричное:", width=12).pack(side=tk.LEFT)
        ttk.Label(hex_frame, textvariable=self.summary_hex, font=("Courier New", 9, "bold"), foreground="darkblue").pack(side=tk.LEFT)
        
        # === ФРЕЙМ ДЛЯ ВИЗУАЛИЗАЦИИ ПЕРЕКЛЮЧАТЕЛЕЙ С ПРОКРУТКОЙ ===
        switches_frame = ttk.LabelFrame(
            main_frame, 
            text="ВИЗУАЛИЗАЦИЯ 32 ПЕРЕКЛЮЧАТЕЛЕЙ (используйте прокрутку колесиком мыши)",
            padding="10"
        )
        switches_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем контейнер с прокруткой для переключателей
        self.create_scrollable_frame(switches_frame)
        
        # Создаем фрейм для легенды (объяснения символов)
        legend_frame = ttk.Frame(switches_frame)
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Легенда для символов переключателей
        legend_label = ttk.Label(
            legend_frame,
            text="● = ВКЛЮЧЕН (1)    ○ = ВЫКЛЮЧЕН (0)    - Используйте колесико мыши для прокрутки",
            font=("Arial", 9),
            foreground="gray"
        )
        legend_label.pack()
    
    def create_scrollable_frame(self, parent):
        """
        Создание прокручиваемой области для переключателей
        """
        # Создаем основной фрейм для всей системы прокрутки
        scroll_main_frame = ttk.Frame(parent)
        scroll_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем холст (canvas) для прокрутки
        self.canvas = tk.Canvas(scroll_main_frame, bg='white')
        
        # Создаем вертикальный скроллбар
        v_scrollbar = ttk.Scrollbar(scroll_main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # Создаем горизонтальный скроллбар
        h_scrollbar = ttk.Scrollbar(scroll_main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        # Настраиваем холст для работы со скроллбарами
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Создаем фрейм, который будет содержать все переключатели и будет прокручиваться
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Создаем окно на холсте для нашего прокручиваемого фрейма
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Размещаем элементы в сетке
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настраиваем веса строк и столбцов для правильного растягивания
        scroll_main_frame.grid_rowconfigure(0, weight=1)
        scroll_main_frame.grid_columnconfigure(0, weight=1)
        
        # Привязываем события для обновления прокрутки
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # УЛУЧШЕННАЯ ПРИВЯЗКА ПРОКРУТКИ КОЛЕСИКОМ МЫШИ
        self.bind_mousewheel_scrolling()
        
    def bind_mousewheel_scrolling(self):
        """
        Привязка прокрутки колесиком мыши ко всем элементам
        """
        # Привязываем прокрутку к холсту
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_mousewheel)    # Linux (прокрутка вверх)
        self.canvas.bind("<Button-5>", self.on_mousewheel)    # Linux (прокрутка вниз)
        
        # Также привязываем прокрутку к самому фрейму для надежности
        self.scrollable_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self.on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self.on_mousewheel)
        
        # Привязываем прокрутку ко всему главному окну, когда курсор над областью переключателей
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)
        
    def _bind_to_mousewheel(self, event):
        """
        Привязываем прокрутку ко всему окну когда курсор над областью переключателей
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)
        
    def _unbind_from_mousewheel(self, event):
        """
        Отвязываем прокрутку когда курсор покидает область переключателей
        """
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        
    def on_frame_configure(self, event):
        """
        Обновляем область прокрутки когда размер фрейма меняется
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """
        Обновляем размер окна на холсте когда размер холста меняется
        """
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        """
        Обработка прокрутки колесом мыши - УЛУЧШЕННАЯ ВЕРСИЯ
        """
        # Определяем платформу и тип события
        if event.delta:  # Windows и Mac
            # Прокручиваем с учетом направления
            scroll_amount = -1 * (event.delta // 120)
            self.canvas.yview_scroll(scroll_amount, "units")
            
        elif event.num in [4, 5]:  # Linux
            # Прокрутка вверх (4) или вниз (5)
            scroll_amount = -1 if event.num == 4 else 1
            self.canvas.yview_scroll(scroll_amount, "units")
            
        return "break"  # Предотвращаем дальнейшую обработку события
    
    def generate_bytes(self):
        """
        Генерация 4 случайных байт и обновление интерфейса
        """
        # Генерируем 4 случайных байта (числа от 0 до 255)
        random_bytes = [random.randint(0, 255) for _ in range(4)]
        
        # Обновляем текстовые представления байтов
        for i, byte_value in enumerate(random_bytes):
            # Устанавливаем десятичное значение байта
            self.byte_vars[i].set(f"Десятичное: {byte_value}")
            
            # Преобразуем в двоичный формат и устанавливаем значение
            binary_str = bin(byte_value)[2:].zfill(8)
            self.binary_vars[i].set(f"Двоичное: {binary_str}")
            
            # ПРЕОБРАЗУЕМ В 16-РИЧНЫЙ ФОРМАТ И УСТАНАВЛИВАЕМ ЗНАЧЕНИЕ
            # hex() возвращает строку вида '0xff', поэтому берем срез [2:] и переводим в верхний регистр
            hex_str = hex(byte_value)[2:].upper().zfill(2)  # zfill(2) добавляет ведущий ноль если нужно
            self.hex_vars[i].set(f"16-ричное: 0x{hex_str}")
        
        # ОБНОВЛЯЕМ СВОДНУЮ ИНФОРМАЦИЮ
        self.update_summary_info(random_bytes)
        
        # Обновляем визуализацию переключателей
        self.update_switches_display(random_bytes)
    
    def update_summary_info(self, bytes_list):
        """
        Обновление сводной информации о всех 4 байтах как едином числе
        """
        # Объединяем 4 байта в одно 32-битное число
        # Каждый следующий байт сдвигаем на 8 бит влево и объединяем
        combined_value = (bytes_list[0] << 24) | (bytes_list[1] << 16) | (bytes_list[2] << 8) | bytes_list[3]
        
        # Десятичное представление
        self.summary_decimal.set(f"{combined_value}")
        
        # Двоичное представление (32 бита)
        binary_32bit = bin(combined_value)[2:].zfill(32)
        # Разбиваем на группы по 8 бит для удобства чтения
        binary_formatted = ' '.join([binary_32bit[i:i+8] for i in range(0, 32, 8)])
        self.summary_binary.set(f"{binary_formatted}")
        
        # 16-РИЧНОЕ ПРЕДСТАВЛЕНИЕ (8 цифр)
        hex_32bit = hex(combined_value)[2:].upper().zfill(8)
        # Разбиваем на группы по 2 цифры для удобства чтения
        hex_formatted = ' '.join([hex_32bit[i:i+2] for i in range(0, 8, 2)])
        self.summary_hex.set(f"0x{hex_formatted}")
    
    def update_switches_display(self, bytes_list):
        """
        Обновление графического отображения переключателей
        """
        # Очищаем предыдущее отображение переключателей
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Счетчик для нумерации всех переключателей
        global_switch_counter = 1
        
        # Создаем визуализацию для каждого байта
        for byte_index, byte_value in enumerate(bytes_list):
            # === СОЗДАЕМ ФРЕЙМ ДЛЯ ОДНОГО БАЙТА (8 ПЕРЕКЛЮЧАТЕЛЕЙ) ===
            byte_frame = ttk.LabelFrame(
                self.scrollable_frame,
                text=f"БАЙТ {byte_index + 1} (переключатели {global_switch_counter}-{global_switch_counter + 7}) - Десятичное: {byte_value}, 16-ричное: 0x{hex(byte_value)[2:].upper().zfill(2)}",
                padding="15"
            )
            byte_frame.pack(fill=tk.X, pady=8, padx=5)
            
            # Преобразуем байт в двоичную строку
            binary_string = bin(byte_value)[2:].zfill(8)
            
            # === ПЕРВАЯ СТРОКА: НОМЕРА ПЕРЕКЛЮЧАТЕЛЕЙ ===
            numbers_frame = ttk.Frame(byte_frame)
            numbers_frame.pack(fill=tk.X, pady=(0, 8))
            
            # Метка "Номера:"
            ttk.Label(numbers_frame, text="Номера:", width=10).pack(side=tk.LEFT)
            
            # Отображаем номера переключателей
            for bit in binary_string:
                switch_num_label = ttk.Label(
                    numbers_frame,
                    text=f"{global_switch_counter:2}",
                    width=4,
                    font=("Arial", 9, "bold"),
                    anchor=tk.CENTER,
                    background="lightgray"
                )
                switch_num_label.pack(side=tk.LEFT, padx=3)
                global_switch_counter += 1
            
            # === ВТОРАЯ СТРОКА: ГРАФИЧЕСКОЕ ПРЕДСТАВЛЕНИЕ ===
            switches_frame = ttk.Frame(byte_frame)
            switches_frame.pack(fill=tk.X, pady=(0, 8))
            
            # Метка "Состояние:"
            ttk.Label(switches_frame, text="Состояние:", width=10).pack(side=tk.LEFT)
            
            # Отображаем графическое состояние переключателей
            for bit in binary_string:
                if bit == '1':
                    # ВКЛЮЧЕННЫЙ переключатель (зеленый кружок с темным фоном)
                    switch_frame = ttk.Frame(switches_frame, relief="raised", borderwidth=1)
                    switch_frame.pack(side=tk.LEFT, padx=3)
                    
                    switch_state_label = ttk.Label(
                        switch_frame,
                        text="●",
                        font=("Arial", 20),
                        foreground="green",
                        width=3,
                        anchor=tk.CENTER,
                        background="black"
                    )
                    switch_state_label.pack(padx=2, pady=2)
                else:
                    # ВЫКЛЮЧЕННЫЙ переключатель (серый кружок со светлым фоном)
                    switch_frame = ttk.Frame(switches_frame, relief="raised", borderwidth=1)
                    switch_frame.pack(side=tk.LEFT, padx=3)
                    
                    switch_state_label = ttk.Label(
                        switch_frame,
                        text="○",
                        font=("Arial", 20),
                        foreground="gray",
                        width=3,
                        anchor=tk.CENTER,
                        background="white"
                    )
                    switch_state_label.pack(padx=2, pady=2)
            
            # === ТРЕТЬЯ СТРОКА: ЧИСЛОВЫЕ ЗНАЧЕНИЯ БИТОВ ===
            bits_frame = ttk.Frame(byte_frame)
            bits_frame.pack(fill=tk.X)
            
            # Метка "Биты:"
            ttk.Label(bits_frame, text="Биты:", width=10).pack(side=tk.LEFT)
            
            # Отображаем числовые значения битов
            for bit in binary_string:
                if bit == '1':
                    # Для единицы - зеленый фон
                    bit_value_label = ttk.Label(
                        bits_frame,
                        text=bit,
                        font=("Arial", 12, "bold"),
                        width=3,
                        anchor=tk.CENTER,
                        background="lightgreen",
                        relief="raised"
                    )
                else:
                    # Для нуля - светлый фон
                    bit_value_label = ttk.Label(
                        bits_frame,
                        text=bit,
                        font=("Arial", 12, "bold"),
                        width=3,
                        anchor=tk.CENTER,
                        background="white",
                        relief="raised"
                    )
                bit_value_label.pack(side=tk.LEFT, padx=3)
        
        # Обновляем область прокрутки после добавления новых элементов
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
    """
    Основная функция для запуска приложения
    """
    # Создаем главное окно
    root = tk.Tk()
    
    # Создаем экземпляр приложения
    app = ByteSwitchApp(root)
    
    # Запускаем главный цикл обработки событий
    root.mainloop()

# Проверяем, запущен ли скрипт напрямую
if __name__ == "__main__":
    # Запускаем приложение
    main()