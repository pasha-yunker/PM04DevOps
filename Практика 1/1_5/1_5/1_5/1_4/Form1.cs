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

            // Настройка TrackBar
            trackBar1.Minimum = 0;
            trackBar1.Maximum = 100;
            trackBar1.Value = 0;
            trackBar1.TickFrequency = 10;

            // Настройка ProgressBar
            progressBar1.Minimum = trackBar1.Minimum;
            progressBar1.Maximum = trackBar1.Maximum;
            progressBar1.Value = trackBar1.Value;

            // Подписываемся на событие изменения TrackBar
            trackBar1.Scroll += TrackBar1_Scroll;

            // Обновляем значение
        }

        private void TrackBar1_Scroll(object sender, EventArgs e)
        {
            // Устанавливаем значение ProgressBar равным TrackBar
            progressBar1.Value = trackBar1.Value;

            // Обновляем текст (если есть Label)
        }

    }
}
