using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            Center();
        }

        private void Center()
        {
            textBox1.Left = (this.ClientSize.Width - textBox1.Width) / 2;
            textBox1.Top = (this.ClientSize.Height - textBox1.Height) / 3;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            textBox1.Text = "Привет, Павел Юнкер!";
            Center();
        }
    }
}
