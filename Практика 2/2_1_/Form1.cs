using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form  
    {
        private bool isFirstImage = true;
        private Image image1;
        private Image image2;
        public Form1()
        {
            InitializeComponent();

            try
            {
                // Просто имена файлов - будут искаться в папке с программой
                image1 = Image.FromFile("vikl2.png");
                image2 = Image.FromFile("vkl2.png");

                button1.BackgroundImage = image1;
                button1.BackgroundImageLayout = ImageLayout.Stretch;
            }
            catch (FileNotFoundException)
            {
                MessageBox.Show("Файлы изображений не найдены! Убедитесь, что vikl2.png и vkl2.png находятся в папке с программой.");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки изображений: {ex.Message}");
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (isFirstImage)
            {
                button1.BackgroundImage = image2;
            }
            else
            {
                button1.BackgroundImage = image1;
            }

            isFirstImage = !isFirstImage;
        }
    }
}
