import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)   # Синус от X
y_cos = np.cos(x)   # Косинус от X

# Построение графиков
plt.figure(figsize=(10, 6))  # Задаем размер графика  

# Меняем название окна
plt.gcf().canvas.manager.set_window_title('Графики sin, cos')

# Рисуем график синуса
plt.plot(x, y_sin, label='sin(x)', color='blue', linewidth=2)

# Рисуем график косинуса
plt.plot(x, y_cos, label='cos(x)', color='red', linewidth=2)

# Добавляем заголовок и подписи осей
plt.title('Графики функций sin(x) и cos(x)')
plt.xlabel('Ось X (радианы)')
plt.ylabel('Ось Y')

# Добавляем сетку для удобства чтения
plt.grid(True, alpha=0.3)  # alpha - прозрачность

# Добавляем легенду
plt.legend()

# Добавляем горизонтальную и вертикальную линии в центре
plt.axhline(y=0, color='black', linewidth=0.5)  # Горизонтальная линия y=0
plt.axvline(x=0, color='black', linewidth=0.5)  # Вертикальная линия x=0

# Показываем график
plt.show()
