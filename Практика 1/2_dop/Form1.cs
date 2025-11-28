using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _2_dop
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            label1.Font = new Font(label1.Font.FontFamily, label1.Font.Size + 1);

            // Центрируем лейбл
            label1.Location = new Point(
                (this.ClientSize.Width - label1.Width) / 2,
                label1.Location.Y
            );
        }
    }
}
