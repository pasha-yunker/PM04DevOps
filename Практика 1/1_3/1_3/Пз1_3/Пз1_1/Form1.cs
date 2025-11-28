using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Пз1_1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            this.Resize += Form1_Resize; // Подписываемся на изменение размера
            CenterControls(); // Центрируем при старте
        }

        private void Form1_Resize(object sender, EventArgs e)
        {
            CenterControls(); // Центрируем при каждом изменении размера
        }

        private void CenterControls()
        {
            // Центрируем кнопку
            button1.Left = (this.ClientSize.Width - button1.Width) / 2;

            // Центрируем лейбл
            label1.Left = (this.ClientSize.Width - label1.Width) / 2;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            int number = int.Parse(label1.Text);
            number += 1;
            string text = number.ToString();
            label1.Text = text;
        }
    }
}
