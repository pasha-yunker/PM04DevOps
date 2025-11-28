import matplotlib.pyplot as plt
import random

num = [random.randint(0, 100) for _ in range(1000)]

plt.scatter(range(1000), num)
plt.gcf().canvas.manager.set_window_title('Точечный график 1000 случайных чисел | Работа Павла Юнкер')
plt.show()