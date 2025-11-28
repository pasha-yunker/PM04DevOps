using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _2_3
{
    public partial class Form1 : Form
    {
        private static Random random = new Random();
        public Form1()
        {
            InitializeComponent();
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            label1.Text = ($"Количество случайных чисел от 0 до 1000: {trackBar1.Value}");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            StringBuilder sb = new StringBuilder();

            for (int i = 0; i < trackBar1.Value; i++)
            {
                int randomNumber = random.Next(0, 101);
                sb.Append(randomNumber);
                sb.Append(" "); // разделитель между числами
            }

            textBox1.Text = sb.ToString();
        }
    }
}

