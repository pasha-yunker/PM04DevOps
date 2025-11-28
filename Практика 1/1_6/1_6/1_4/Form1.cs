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
                Label label = Controls.Find($"label{i}", true).FirstOrDefault() as Label;
                Panel panel = Controls.Find($"panel{i}", true).FirstOrDefault() as Panel;

                if (label != null && panel != null)
                {
                    if (pr <= max) // Все значения до максимального включительно
                    {
                        panel.BackColor = Color.Green;
                        if (pr == max) // Только для максимального показываем лейбл
                        {
                            label.Visible = true;
                            label.Text = $"{pr} %";
                        }
                        else
                        {
                            label.Visible = false;
                            label.Text = "";
                        }
                    }
                    else // Значения больше максимального
                    {
                        label.Visible = false;
                        label.Text = "";
                        panel.BackColor = Color.Red;
                    }
                }
            }
        }
    }
}
