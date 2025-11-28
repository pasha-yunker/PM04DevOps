using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _1_4_
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            textBox2.Text = Convert.ToString(trackBar1.Value);
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(textBox2.Text))
            {
                if (!int.TryParse(textBox2.Text, out int n))
                {
                    MessageBox.Show("Введите число");
                    return;
                }

                if (n > 100)
                {
                    MessageBox.Show("Введите число меньше 100!");
                    return;
                }

                trackBar1.Value = n;

            }

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            if (!string.IsNullOrEmpty(textBox1.Text))
            {
                if (!int.TryParse(textBox1.Text, out int n))
                {
                    MessageBox.Show("Введите число");
                    return;
                }

                if (n > 100)
                {
                    MessageBox.Show("Введите число меньше 100!");
                    return;
                }


                progressBar1.Value = n;
            }
        }
    }
}
