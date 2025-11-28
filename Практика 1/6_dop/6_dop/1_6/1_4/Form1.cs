using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _1_4
{
    public partial class Form1 : Form
    {
        private Random random = new Random();
        public Form1()
        {
            InitializeComponent();
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            int max = 0;

            // Находим максимальное достигнутое значение
            for (int i = 1; i <= 10; i++)
            {
                int pr = i * 10;
                if (trackBar1.Value >= pr)
                {
                    max = pr;
                }
            }

            // Обновляем все элементы
            for (int i = 1; i <= 10; i++)
            {
                int pr = i * 10;

                Panel panel = Controls.Find($"panel{i}", true).FirstOrDefault() as Panel;

                if (panel != null)
                {
                    if (pr <= max) // Все значения до максимального включительно
                    {
                        panel.BackColor = Color.Green;

                    }
                    else // Значения больше максимального
                    {

                        panel.BackColor = Color.White;
                    }
                }
                if (trackBar1.Value > 80)
                {
                    panel9.BackColor = Color.Red;
                }
                if (trackBar1.Value > 90)
                {
                    panel10.BackColor = Color.Red;
                }
            }
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            int max = 0;

            // Находим максимальное достигнутое значение
            for (int i = 1; i <= 10; i++)
            {
                int pr = i * 10;
                if (trackBar2.Value >= pr)
                {
                    max = pr;
                }
            }

            // Обновляем все элементы
            for (int i = 1; i <= 10; i++)
            {
                int pr = i * 10;

                Panel pane = Controls.Find($"pane{i}", true).FirstOrDefault() as Panel;

                if (pane != null)
                {
                    if (pr <= max) // Все значения до максимального включительно
                    {
                        pane.BackColor = Color.Green;

                    }
                    else // Значения больше максимального
                    {

                        pane.BackColor = Color.White;
                    }
                }
                if (trackBar2.Value > 80)
                {
                    pane9.BackColor = Color.Red;
                }
                if (trackBar2.Value > 90)
                {
                    pane10.BackColor = Color.Red;
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            trackBar1.Value = random.Next(trackBar1.Minimum, trackBar1.Maximum + 1);
            trackBar2.Value = random.Next(trackBar2.Minimum, trackBar2.Maximum + 1);
            trackBar1_Scroll(null, EventArgs.Empty);
            trackBar2_Scroll(null, EventArgs.Empty);
        }
    }
}