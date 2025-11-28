using System;
using System.Drawing;
using System.Windows.Forms;

namespace PrinterConnectionApp
{
    public partial class Form1 : Form
    {
        private Panel mainPanel;
        private PictureBox printerPictureBox;
        private Label statusLabel;
        private Button infoButton;
        private Button usbButton;
        private Button wifiButton;
        private Button bluetoothButton;
        private Button connectButton;

        private string selectedMethod = null;

        public Form1()
        {
            InitializeComponent();
            InitializeEvents();
        }

        private void InitializeComponent()
        {
            // Основная форма
            this.SuspendLayout();
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(650, 500);
            this.Text = "Подключение принтера | Работа Павла Юнкер";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(245, 245, 255); // Более мягкий голубой
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;

            // Главная панель
            this.mainPanel = new System.Windows.Forms.Panel();
            this.mainPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.mainPanel.BackColor = Color.FromArgb(245, 245, 255);

            // Картинка принтера
            this.printerPictureBox = new System.Windows.Forms.PictureBox();
            this.printerPictureBox.Size = new System.Drawing.Size(220, 170);
            this.printerPictureBox.Location = new System.Drawing.Point(215, 50);
            this.printerPictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.printerPictureBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.printerPictureBox.BackColor = Color.White;

            // Кнопка информации
            this.infoButton = new System.Windows.Forms.Button();
            this.infoButton.Size = new System.Drawing.Size(35, 35);
            this.infoButton.Location = new System.Drawing.Point(605, 10);
            this.infoButton.Text = "?";
            this.infoButton.Font = new System.Drawing.Font("Arial", 14F, System.Drawing.FontStyle.Bold);
            this.infoButton.BackColor = System.Drawing.Color.FromArgb(200, 220, 255); // Светло-синий
            this.infoButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.infoButton.Cursor = Cursors.Hand;

            // Кнопка USB (расположена горизонтально)
            this.usbButton = new System.Windows.Forms.Button();
            this.usbButton.Size = new System.Drawing.Size(180, 45);
            this.usbButton.Location = new System.Drawing.Point(50, 260);
            this.usbButton.Text = "USB-кабель";
            this.usbButton.Font = new System.Drawing.Font("Arial", 11F);
            this.usbButton.BackColor = Color.FromArgb(240, 240, 240); // Светло-серый
            this.usbButton.FlatStyle = FlatStyle.Flat;
            this.usbButton.Cursor = Cursors.Hand;

            // Кнопка Wi-Fi (расположена горизонтально)
            this.wifiButton = new System.Windows.Forms.Button();
            this.wifiButton.Size = new System.Drawing.Size(180, 45);
            this.wifiButton.Location = new System.Drawing.Point(235, 260);
            this.wifiButton.Text = "Wi-Fi подключение";
            this.wifiButton.Font = new System.Drawing.Font("Arial", 11F);
            this.wifiButton.BackColor = Color.FromArgb(240, 240, 240); // Светло-серый
            this.wifiButton.FlatStyle = FlatStyle.Flat;
            this.wifiButton.Cursor = Cursors.Hand;

            // Кнопка Bluetooth (расположена горизонтально)
            this.bluetoothButton = new System.Windows.Forms.Button();
            this.bluetoothButton.Size = new System.Drawing.Size(180, 45);
            this.bluetoothButton.Location = new System.Drawing.Point(420, 260);
            this.bluetoothButton.Text = "Bluetooth подключение";
            this.bluetoothButton.Font = new System.Drawing.Font("Arial", 11F);
            this.bluetoothButton.BackColor = Color.FromArgb(240, 240, 240); // Светло-серый
            this.bluetoothButton.FlatStyle = FlatStyle.Flat;
            this.bluetoothButton.Cursor = Cursors.Hand;

            // Кнопка подключения
            this.connectButton = new System.Windows.Forms.Button();
            this.connectButton.Size = new System.Drawing.Size(180, 50);
            this.connectButton.Location = new System.Drawing.Point(235, 360);
            this.connectButton.Text = "Подключить";
            this.connectButton.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Bold);
            this.connectButton.BackColor = System.Drawing.Color.FromArgb(220, 240, 220); // Светло-зеленый
            this.connectButton.FlatStyle = FlatStyle.Flat;
            this.connectButton.Cursor = Cursors.Hand;

            // Статусная метка
            this.statusLabel = new System.Windows.Forms.Label();
            this.statusLabel.Size = new System.Drawing.Size(450, 35);
            this.statusLabel.Location = new System.Drawing.Point(100, 445);
            this.statusLabel.Text = "Выберите способ подключения";
            this.statusLabel.Font = new System.Drawing.Font("Arial", 12F, System.Drawing.FontStyle.Bold);
            this.statusLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.statusLabel.BackColor = System.Drawing.Color.FromArgb(240, 240, 240); // Серый по умолчанию
            this.statusLabel.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;

            // Добавление элементов на панель
            this.mainPanel.Controls.Add(this.printerPictureBox);
            this.mainPanel.Controls.Add(this.infoButton);
            this.mainPanel.Controls.Add(this.usbButton);
            this.mainPanel.Controls.Add(this.wifiButton);
            this.mainPanel.Controls.Add(this.bluetoothButton);
            this.mainPanel.Controls.Add(this.connectButton);
            this.mainPanel.Controls.Add(this.statusLabel);

            this.Controls.Add(this.mainPanel);

            // Установка картинки принтера
            SetPrinterImage();

            this.ResumeLayout(false);
        }

        private void SetPrinterImage()
        {
            // Создаем простую картинку принтера программно
            Bitmap printerBitmap = new Bitmap(220, 170);
            using (Graphics g = Graphics.FromImage(printerBitmap))
            {
                g.Clear(Color.White);
                using (Pen pen = new Pen(Color.Black, 2))
                {
                    // Корпус принтера
                    g.DrawRectangle(pen, 60, 50, 100, 70);
                    // Лоток для бумаги
                    g.DrawRectangle(pen, 70, 120, 80, 25);
                    // Кнопки
                    g.FillEllipse(Brushes.Red, 170, 60, 12, 12);
                    g.FillEllipse(Brushes.Green, 170, 85, 12, 12);
                }
            }
            this.printerPictureBox.Image = printerBitmap;
        }

        private void InitializeEvents()
        {
            // Обработчик для кнопки информации
            this.infoButton.Click += InfoButton_Click;

            // Обработчик для кнопки подключения
            this.connectButton.Click += ConnectButton_Click;

            // Обработчики для кнопок выбора способа подключения
            this.usbButton.Click += ConnectionButton_Click;
            this.wifiButton.Click += ConnectionButton_Click;
            this.bluetoothButton.Click += ConnectionButton_Click;
        }

        private void ConnectionButton_Click(object sender, EventArgs e)
        {
            // Сбрасываем цвет всех кнопок
            usbButton.BackColor = Color.FromArgb(240, 240, 240);
            wifiButton.BackColor = Color.FromArgb(240, 240, 240);
            bluetoothButton.BackColor = Color.FromArgb(240, 240, 240);

            // Устанавливаем цвет выбранной кнопки
            Button clickedButton = (Button)sender;
            clickedButton.BackColor = Color.FromArgb(180, 220, 240); // Голубоватый цвет для выбора

            // Запоминаем выбранный метод
            selectedMethod = clickedButton.Text;

            UpdateStatus($"Выбран способ: {clickedButton.Text}", Color.FromArgb(220, 230, 240));
        }

        private void ConnectButton_Click(object sender, EventArgs e)
        {
            // Проверяем, выбран ли способ подключения
            if (string.IsNullOrEmpty(selectedMethod))
            {
                UpdateStatus("❌ Выберите способ подключения!", Color.FromArgb(255, 220, 220)); // Светло-красный
                return;
            }

            // Имитация процесса подключения
            UpdateStatus("⏳ Подключаемся...", Color.FromArgb(255, 255, 200)); // Светло-желтый

            // Задержка для имитации процесса подключения
            Timer timer = new Timer();
            timer.Interval = 2000;
            timer.Tick += (s, args) =>
            {
                timer.Stop();
                timer.Dispose();

                // Имитация результата подключения
                Random rnd = new Random();
                int result = rnd.Next(1, 4);

                switch (result)
                {
                    case 1:
                        UpdateStatus("✓ Успешно подключено!", Color.FromArgb(220, 255, 220)); // Светло-зеленый
                        break;
                    case 2:
                        UpdateStatus("✗ Ошибка подключения", Color.FromArgb(255, 220, 220)); // Светло-красный
                        break;
                    case 3:
                        UpdateStatus("! Нет бумаги", Color.FromArgb(255, 235, 180)); // Светло-оранжевый
                        break;
                }
            };
            timer.Start();
        }

        private void InfoButton_Click(object sender, EventArgs e)
        {
            string infoMessage = @"Информация о программе:

Кнопки подключения:
- USB-кабель: Подключение через USB-порт
- Wi-Fi: Беспроводное подключение по сети
- Bluetooth: Беспроводное подключение Bluetooth

Статусы:
✓ Готово/Успешно - светло-зеленый
! Предупреждение (нет бумаги) - светло-оранжевый
✗ Ошибка - светло-красный
⏳ Подключение - светло-желтый
❌ Не выбрано - светло-красный

Нажмите 'Подключить' для начала процесса.";

            MessageBox.Show(infoMessage, "Справка по программе",
                MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void UpdateStatus(string message, Color color)
        {
            statusLabel.Text = message;
            statusLabel.BackColor = color;
        }
    }

    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}