using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _1_9
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            UpdateColor();
        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            UpdateColor();
        }

        private void trackBar3_Scroll(object sender, EventArgs e)
        {
            UpdateColor();
        }

        private void UpdateColor()
        {
            // Берем значения с всех трех трекбаров
            int r = trackBar1.Value;
            int g = trackBar2.Value;
            int b = trackBar3.Value;

            // Создаем цвет и применяем к панели
            panel1.BackColor = Color.FromArgb(r, g, b);

            // Опционально: выводим значения RGB
            label1.Text = $"R: {r} G: {g} B: {b}";
        }

        

    }
}
