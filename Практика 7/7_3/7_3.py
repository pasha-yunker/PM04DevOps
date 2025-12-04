import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.widgets import TextBox, Button
import sys
import os

# Для PyInstaller
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

class ElectricCharge:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
    
    def electric_field(self, x, y):
        dx = x - self.x
        dy = y - self.y
        r = np.sqrt(dx**2 + dy**2)
        
        if r == 0:
            return 0, 0
            
        k = 9e9
        E_magnitude = k * abs(self.charge) / r**2
        E_x = E_magnitude * dx / r
        E_y = E_magnitude * dy / r
        
        if self.charge < 0:
            E_x = -E_x
            E_y = -E_y
            
        return E_x, E_y

class InteractiveChargeSimulation:
    def __init__(self):
        self.charges = []
        self.fig = None
        self.ax_plot = None
        self.quiver = None
        self.charge_circles = []
        self.charge_texts = []
        
        self.textbox_x = None
        self.textbox_y = None
        self.textbox_charge = None
        self.button_add = None
        self.button_clear = None
        
        self.setup_interface()
    
    def add_charge(self, x, y, charge):
        self.charges.append(ElectricCharge(x, y, charge))
        self.update_plot()
    
    def clear_charges(self):
        self.charges = []
        self.update_plot()
    
    def total_electric_field(self, x, y):
        E_total_x = 0
        E_total_y = 0
        
        for charge in self.charges:
            E_x, E_y = charge.electric_field(x, y)
            E_total_x += E_x
            E_total_y += E_y
            
        return E_total_x, E_total_y
    
    def setup_interface(self):
        self.fig = plt.figure(figsize=(12, 10))
        self.fig.canvas.manager.set_window_title('Симулятор электрического поля | Работа Павла Юнкер')
        
        self.ax_plot = plt.axes([0.1, 0.2, 0.8, 0.7])
        
        self.create_control_panel()
        self.setup_plots()
        self.connect_events()
    
    def create_control_panel(self):
        ax_x = plt.axes([0.1, 0.1, 0.15, 0.05])
        self.textbox_x = TextBox(ax_x, 'X: ', initial='0.0')
        
        ax_y = plt.axes([0.3, 0.1, 0.15, 0.05])
        self.textbox_y = TextBox(ax_y, 'Y: ', initial='0.0')
        
        ax_charge = plt.axes([0.5, 0.1, 0.15, 0.05])
        self.textbox_charge = TextBox(ax_charge, 'Заряд: ', initial='1e-9')
        
        ax_add = plt.axes([0.7, 0.1, 0.1, 0.05])
        self.button_add = Button(ax_add, 'Добавить')
        
        ax_clear = plt.axes([0.82, 0.1, 0.08, 0.05])
        self.button_clear = Button(ax_clear, 'Очистить')
    
    def setup_plots(self):
        self.ax_plot.set_xlim(-5, 5)
        self.ax_plot.set_ylim(-5, 5)
        self.ax_plot.set_aspect('equal')
        self.ax_plot.set_xlabel('X координата (м)')
        self.ax_plot.set_ylabel('Y координата (м)')
        self.ax_plot.set_title('Электрическое поле точечных зарядов')
        self.ax_plot.grid(True, alpha=0.3)
    
    def connect_events(self):
        self.button_add.on_clicked(self.on_add_button_clicked)
        self.button_clear.on_clicked(self.on_clear_clicked)
        
        self.textbox_x.on_submit(self.on_text_changed)
        self.textbox_y.on_submit(self.on_text_changed)
        self.textbox_charge.on_submit(self.on_text_changed)
    
    def on_text_changed(self, text):
        pass
    
    def on_add_button_clicked(self, event):
        self.add_charge_from_inputs()
    
    def on_clear_clicked(self, event):
        self.clear_charges()
    
    def add_charge_from_inputs(self):
        try:
            x = float(self.textbox_x.text)
            y = float(self.textbox_y.text)
            charge = float(self.textbox_charge.text)
            self.add_charge(x, y, charge)
        except ValueError:
            # В EXE-версии лучше не использовать print
            pass
    
    def update_plot(self):
        if self.quiver is not None:
            self.quiver.remove()
            self.quiver = None
        
        for circle in self.charge_circles:
            circle.remove()
        self.charge_circles = []
        
        for text in self.charge_texts:
            text.remove()
        self.charge_texts = []
        
        grid_points = 15
        x = np.linspace(-5, 5, grid_points)
        y = np.linspace(-5, 5, grid_points)
        X, Y = np.meshgrid(x, y)
        
        U, V = np.zeros(X.shape), np.zeros(Y.shape)
        for i in range(len(x)):
            for j in range(len(y)):
                E_x, E_y = self.total_electric_field(X[j,i], Y[j,i])
                U[j,i] = E_x
                V[j,i] = E_y
        
        magnitude = np.sqrt(U**2 + V**2)
        non_zero_mask = magnitude > 0
        U_norm = np.zeros_like(U)
        V_norm = np.zeros_like(V)
        
        U_norm[non_zero_mask] = U[non_zero_mask] / magnitude[non_zero_mask]
        V_norm[non_zero_mask] = V[non_zero_mask] / magnitude[non_zero_mask]
        
        self.quiver = self.ax_plot.quiver(X, Y, U_norm, V_norm, 
                                         color='blue', alpha=0.6, 
                                         scale=20, width=0.005)
        
        for charge in self.charges:
            color = 'red' if charge.charge > 0 else 'blue'
            circle = Circle((charge.x, charge.y), 0.2, color=color, alpha=0.8)
            self.ax_plot.add_patch(circle)
            self.charge_circles.append(circle)
            
            sign = '+' if charge.charge > 0 else '-'
            text = self.ax_plot.text(charge.x, charge.y, sign, 
                                   ha='center', va='center', 
                                   color='white', fontweight='bold',
                                   fontsize=10)
            self.charge_texts.append(text)
        
        title = f'Электрическое поле (зарядов: {len(self.charges)})'
        self.ax_plot.set_title(title)
        self.fig.canvas.draw_idle()
    
    def show(self):
        plt.show()

if __name__ == "__main__":
    sim = InteractiveChargeSimulation()
    sim.show()
