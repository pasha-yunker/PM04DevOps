using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _2_1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Random random = new Random();
            StringBuilder sb = new StringBuilder();

            int numbersPerLine = 37; // Количество чисел в одной строке

            for (int i = 0; i < 1000; i++)
            {
                int number = random.Next(0, 101);
                sb.Append(number.ToString().PadLeft(3) + " "); // Добавляем пробел

                // Перенос строки после каждого numbersPerLine чисел
                if ((i + 1) % numbersPerLine == 0)
                {
                    sb.AppendLine();
                }
            }

            textBox1.Text = sb.ToString();
        }
    }
}
