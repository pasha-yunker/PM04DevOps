import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush

class Speedometer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.speed = 0
        
    def set_speed(self, value):
        self.speed = max(0, min(240, value))
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Центр и радиус
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 20
        
        # Фон
        painter.setPen(QPen(QColor(44, 62, 80), 8))
        painter.setBrush(QBrush(QColor(236, 240, 241)))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Внутренний круг
        painter.setPen(QPen(QColor(189, 195, 199), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(center_x - radius + 10, center_y - radius + 10, 
                          (radius - 10) * 2, (radius - 10) * 2)
        
        # Шкала
        self.draw_scale(painter, center_x, center_y, radius)
        
        # Стрелка
        self.draw_needle(painter, center_x, center_y, radius - 40)
        
        # Центр
        painter.setPen(QPen(QColor(192, 57, 43), 2))
        painter.setBrush(QBrush(QColor(231, 76, 60)))
        painter.drawEllipse(center_x - 6, center_y - 6, 12, 12)
        
        # Текущая скорость
        '''painter.setFont(QFont('Arial', 16, QFont.Bold))
        painter.setPen(QColor(44, 62, 80))
        painter.drawText(center_x - 25, center_y - 8, 50, 20, 
                        Qt.AlignCenter, f"{int(self.speed)}")'''
        
        painter.setFont(QFont('Arial', 12))
        painter.drawText(center_x - 25, center_y + 15, 50, 20, 
                        Qt.AlignCenter, "км/ч")

    def draw_scale(self, painter, cx, cy, radius):
        # Основные цифры
        numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]
        start_angle = 135
        end_angle = 405  # 135 + 270
        
        for number in numbers:
            # Угол для этого числа
            angle = start_angle + (number / 240) * 270
            rad = math.radians(angle)
            
            # Деление
            x1 = cx + math.cos(rad) * (radius - 15)
            y1 = cy + math.sin(rad) * (radius - 15)
            x2 = cx + math.cos(rad) * radius
            y2 = cy + math.sin(rad) * radius
            
            painter.setPen(QPen(QColor(44, 62, 80), 3))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
            # Цифра
            label_radius = radius - 30
            label_x = cx + math.cos(rad) * label_radius
            label_y = cy + math.sin(rad) * label_radius
            
            painter.setPen(QColor(44, 62, 80))
            painter.setFont(QFont('Arial', 12, QFont.Bold))
            painter.drawText(int(label_x - 12), int(label_y - 6), 24, 12, 
                           Qt.AlignCenter, str(number))
        
        # Мелкие деления
        for number in range(0, 241, 10):
            if number not in numbers:
                angle = start_angle + (number / 240) * 270
                rad = math.radians(angle)
                
                x1 = cx + math.cos(rad) * (radius - 10)
                y1 = cy + math.sin(rad) * (radius - 10)
                x2 = cx + math.cos(rad) * radius
                y2 = cy + math.sin(rad) * radius
                
                painter.setPen(QPen(QColor(127, 140, 141), 1))
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_needle(self, painter, cx, cy, length):
        angle = 135 + (self.speed / 240) * 270
        rad = math.radians(angle)
        
        end_x = cx + math.cos(rad) * length
        end_y = cy + math.sin(rad) * length
        
        painter.setPen(QPen(QColor(231, 76, 60), 4))
        painter.drawLine(cx, cy, int(end_x), int(end_y))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Спидометр | Работа Павла Юнкер")
        self.setGeometry(100, 100, 450, 550)
        
        layout = QVBoxLayout()
        
        # Спидометр
        self.speedometer = Speedometer()
        layout.addWidget(self.speedometer)
        
        # Слайдер
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(240)
        self.slider.valueChanged.connect(self.speedometer.set_speed)
        layout.addWidget(self.slider)
        
        # Метка
        self.label = QLabel("Скорость: 0 км/ч")
        self.label.setAlignment(Qt.AlignCenter)
        self.slider.valueChanged.connect(lambda v: self.label.setText(f"Скорость: {v} км/ч"))
        layout.addWidget(self.label)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())