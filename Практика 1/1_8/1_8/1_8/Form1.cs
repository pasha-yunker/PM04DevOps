using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _1_8
{
    public partial class Form1 : Form
    {
        private Random random = new Random();

        public Form1()
        {
            InitializeComponent();

            trackMin.Scroll += TrackBars_Scroll;
            trackMax.Scroll += TrackBars_Scroll;
            button1.Click += ButtonReset_Click;

            GenerateRandomValue();
        }

        private void TrackBars_Scroll(object sender, EventArgs e)
        {
            // Проверяем, чтобы min <= max
            if (trackMin.Value > trackMax.Value)
            {
                trackMin.Value = trackMax.Value;
            }
            
        }

        private void GenerateRandomValue()
        {
            int randomValue = random.Next(trackMin.Value, trackMax.Value + 1);
            progressBar1.Value = randomValue;
            label1.Text = $"Диапазон: [{trackMin.Value}-{trackMax.Value}]\nЗначение: {randomValue}";
        }

        private void ButtonReset_Click(object sender, EventArgs e)
        {
            trackMin.Value = 0;
            trackMax.Value = 100;
            GenerateRandomValue();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            GenerateRandomValue();
        }
    }
}