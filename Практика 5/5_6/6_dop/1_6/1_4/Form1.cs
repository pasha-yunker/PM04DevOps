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
            // Инициализация при загрузке формы
            UpdatePanels(trackBar1.Value, "panel");
            UpdatePanels(trackBar2.Value, "pane");
        }

        private void UpdatePanels(int trackBarValue, string panelPrefix)
        {
            // Рассчитываем количество горящих панелей
            int panelsToLight = (int)Math.Ceiling(trackBarValue / 27.0 * 27);

            for (int i = 1; i <= 27; i++)
            {
                Panel panel = Controls.Find($"{panelPrefix}{i}", true).FirstOrDefault() as Panel;

                if (panel != null)
                {
                    if (i <= panelsToLight)
                    {
                        // От 22 до 27 - красный, остальные - зеленый
                        if (i >= 22 && i <= 27)
                        {
                            panel.BackColor = Color.Red;
                        }
                        else
                        {
                            panel.BackColor = Color.Green;
                        }
                    }
                    else
                    {
                        panel.BackColor = Color.White;
                    }
                }
            }
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            UpdatePanels(trackBar1.Value, "panel");
        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            UpdatePanels(trackBar2.Value, "pane");
        }

        private void label2_Click(object sender, EventArgs e)
        {
            // Ваш код для label2
        }
    




        private void button1_Click(object sender, EventArgs e)
        {
            trackBar1.Value = random.Next(trackBar1.Minimum, trackBar1.Maximum + 1);
            trackBar2.Value = random.Next(trackBar2.Minimum, trackBar2.Maximum + 1);
            trackBar1_Scroll(null, EventArgs.Empty);
            trackBar2_Scroll(null, EventArgs.Empty);
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}