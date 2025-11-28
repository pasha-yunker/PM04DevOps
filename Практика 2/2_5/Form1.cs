using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _2_2
{
    public partial class Form1 : Form
    {
        private static Random random = new Random();
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            int min = trackBar1.Value;
            int max = trackBar2.Value;

            int randomNumber = random.Next(min, max + 1);

            label1.Text = $"{randomNumber}";
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            if (trackBar1.Value > trackBar2.Value)
            {
                trackBar2.Value = trackBar1.Value;
            }
            label2.Text = $"{trackBar1.Value}";
            label3.Text = $"{trackBar2.Value}";
        }

        private void trackBar2_Scroll(object sender, EventArgs e)
        {
            if (trackBar2.Value < trackBar1.Value)
            {
                trackBar2.Value = trackBar1.Value;
            }
            label2.Text = $"{trackBar1.Value}";
            label3.Text = $"{trackBar2.Value}";
        }
    }
}
