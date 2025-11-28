using System;
using System.Drawing;
using System.Windows.Forms;
using System.Globalization;

namespace MobileCalendar
{
    public partial class Form1 : Form
    {
        private DateTime currentDate;
        private DateTime selectedDate;
        private Label monthYearLabel;
        private Label currentDateLabel;
        private Label selectedDateLabel;
        private TableLayoutPanel calendarGrid;
        private Panel headerPanel;
        private Panel daysPanel;
        private Panel bottomPanel;
        private Panel[,] dayCells; // Массив для хранения ссылок на ячейки

        public Form1()
        {
            InitializeComponent();
            InitializeCustomComponents();
        }

        private void InitializeCustomComponents()
        {
            this.Text = "📅 Мобильный Календарь";
            this.Size = new Size(400, 650);
            this.BackColor = Color.FromArgb(240, 240, 240);
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;

            currentDate = DateTime.Now;
            selectedDate = DateTime.Now;
            dayCells = new Panel[6, 7]; // 6 строк, 7 столбцов

            CreateHeader();
            CreateDaysOfWeek();
            CreateCalendarGrid();
            CreateBottomPanel();
            UpdateCalendar();
        }

        private void CreateHeader()
        {
            headerPanel = new Panel();
            headerPanel.BackColor = Color.FromArgb(66, 133, 244);
            headerPanel.Size = new Size(400, 100);
            headerPanel.Location = new Point(0, 0);
            this.Controls.Add(headerPanel);

            // Кнопка предыдущего месяца
            Button prevBtn = new Button();
            prevBtn.Text = "◀";
            prevBtn.Font = new Font("Arial", 16, FontStyle.Bold);
            prevBtn.BackColor = Color.FromArgb(51, 103, 214);
            prevBtn.ForeColor = Color.White;
            prevBtn.FlatStyle = FlatStyle.Flat;
            prevBtn.Size = new Size(40, 40);
            prevBtn.Location = new Point(15, 20);
            prevBtn.Click += (s, e) => PrevMonth();
            headerPanel.Controls.Add(prevBtn);

            // Кнопка следующего месяца
            Button nextBtn = new Button();
            nextBtn.Text = "▶";
            nextBtn.Font = new Font("Arial", 16, FontStyle.Bold);
            nextBtn.BackColor = Color.FromArgb(51, 103, 214);
            nextBtn.ForeColor = Color.White;
            nextBtn.FlatStyle = FlatStyle.Flat;
            nextBtn.Size = new Size(40, 40);
            nextBtn.Location = new Point(345, 20);
            nextBtn.Click += (s, e) => NextMonth();
            headerPanel.Controls.Add(nextBtn);

            // Метка месяца и года
            monthYearLabel = new Label();
            monthYearLabel.Font = new Font("Arial", 20, FontStyle.Bold);
            monthYearLabel.ForeColor = Color.White;
            monthYearLabel.BackColor = Color.Transparent;
            monthYearLabel.TextAlign = ContentAlignment.MiddleCenter;
            monthYearLabel.Size = new Size(250, 30);
            monthYearLabel.Location = new Point(75, 15);
            headerPanel.Controls.Add(monthYearLabel);

            // Заголовок "Сегодня"
            Label todayTitle = new Label();
            todayTitle.Text = "СЕГОДНЯ:";
            todayTitle.Font = new Font("Arial", 10, FontStyle.Bold);
            todayTitle.ForeColor = Color.FromArgb(232, 240, 254);
            todayTitle.BackColor = Color.Transparent;
            todayTitle.TextAlign = ContentAlignment.MiddleCenter;
            todayTitle.Size = new Size(100, 20);
            todayTitle.Location = new Point(150, 45);
            headerPanel.Controls.Add(todayTitle);

            // Текущая дата (сегодня)
            currentDateLabel = new Label();
            currentDateLabel.Font = new Font("Arial", 14, FontStyle.Bold);
            currentDateLabel.ForeColor = Color.White;
            currentDateLabel.BackColor = Color.Transparent;
            currentDateLabel.TextAlign = ContentAlignment.MiddleCenter;
            currentDateLabel.Size = new Size(250, 25);
            currentDateLabel.Location = new Point(75, 65);
            headerPanel.Controls.Add(currentDateLabel);
        }

        private void CreateDaysOfWeek()
        {
            daysPanel = new Panel();
            daysPanel.BackColor = Color.FromArgb(240, 240, 240);
            daysPanel.Size = new Size(370, 30);
            daysPanel.Location = new Point(15, 110);
            this.Controls.Add(daysPanel);

            string[] days = { "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс" };
            int totalWidth = 370;
            int cellWidth = totalWidth / 7; // Равномерно распределяем по ширине панели

            for (int i = 0; i < days.Length; i++)
            {
                Label dayLabel = new Label();
                dayLabel.Text = days[i];
                dayLabel.Font = new Font("Arial", 12, FontStyle.Bold);
                dayLabel.ForeColor = (i == 5 || i == 6) ? Color.FromArgb(255, 68, 68) : Color.FromArgb(102, 102, 102);
                dayLabel.BackColor = Color.Transparent;
                dayLabel.TextAlign = ContentAlignment.MiddleCenter;
                dayLabel.Size = new Size(cellWidth, 25);
                dayLabel.Location = new Point(i * cellWidth, 2); // Центрируем по вертикали
                daysPanel.Controls.Add(dayLabel);
            }
        }

        private void CreateCalendarGrid()
        {
            calendarGrid = new TableLayoutPanel();
            calendarGrid.BackColor = Color.FromArgb(240, 240, 240);
            calendarGrid.Size = new Size(370, 350);
            calendarGrid.Location = new Point(15, 150);
            calendarGrid.ColumnCount = 7;
            calendarGrid.RowCount = 6;

            for (int i = 0; i < 7; i++)
            {
                calendarGrid.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100f / 7));
            }
            for (int i = 0; i < 6; i++)
            {
                calendarGrid.RowStyles.Add(new RowStyle(SizeType.Percent, 100f / 6));
            }

            this.Controls.Add(calendarGrid);
        }

        private void CreateBottomPanel()
        {
            bottomPanel = new Panel();
            bottomPanel.BackColor = Color.White;
            bottomPanel.Size = new Size(400, 120);
            bottomPanel.Location = new Point(0, 520);
            this.Controls.Add(bottomPanel);

            // Выбранная дата
            Label selectedTitle = new Label();
            selectedTitle.Text = "ВЫБРАНА ДАТА:";
            selectedTitle.Font = new Font("Arial", 10, FontStyle.Bold);
            selectedTitle.ForeColor = Color.FromArgb(102, 102, 102);
            selectedTitle.BackColor = Color.Transparent;
            selectedTitle.Size = new Size(150, 20);
            selectedTitle.Location = new Point(20, 15);
            bottomPanel.Controls.Add(selectedTitle);

            selectedDateLabel = new Label();
            selectedDateLabel.Font = new Font("Arial", 18, FontStyle.Bold);
            selectedDateLabel.ForeColor = Color.FromArgb(66, 133, 244);
            selectedDateLabel.BackColor = Color.Transparent;
            selectedDateLabel.Size = new Size(300, 30);
            selectedDateLabel.Location = new Point(20, 40);
            bottomPanel.Controls.Add(selectedDateLabel);
        }

        private void UpdateCalendar()
        {
            // Обновляем заголовок
            string monthName = GetMonthName(currentDate.Month);
            monthYearLabel.Text = $"{monthName} {currentDate.Year}";

            // Обновляем сегодняшнюю дату
            currentDateLabel.Text = DateTime.Now.ToString("dd MMMM yyyy", new CultureInfo("ru-RU"));

            // Очищаем сетку календаря
            calendarGrid.Controls.Clear();

            // Получаем календарь на текущий месяц
            DateTime firstDayOfMonth = new DateTime(currentDate.Year, currentDate.Month, 1);
            int daysInMonth = DateTime.DaysInMonth(currentDate.Year, currentDate.Month);
            int firstDayOfWeek = ((int)firstDayOfMonth.DayOfWeek + 6) % 7;

            int row = 0;
            int col = firstDayOfWeek;

            for (int day = 1; day <= daysInMonth; day++)
            {
                DateTime cellDate = new DateTime(currentDate.Year, currentDate.Month, day);
                bool isToday = cellDate.Date == DateTime.Now.Date;
                bool isSelected = cellDate.Date == selectedDate.Date;

                Panel dayCell = CreateDayCell(day, isToday, isSelected, cellDate, row, col);
                calendarGrid.Controls.Add(dayCell, col, row);
                dayCells[row, col] = dayCell;

                col++;
                if (col > 6)
                {
                    col = 0;
                    row++;
                }
            }

            // Обновляем нижнюю панель
            UpdateBottomPanel();
        }

        private Panel CreateDayCell(int day, bool isToday, bool isSelected, DateTime cellDate, int row, int col)
        {
            Panel cell = new Panel();
            cell.Size = new Size(50, 50);
            cell.Margin = new Padding(2);
            cell.Cursor = Cursors.Hand;
            cell.Tag = new DateTime(currentDate.Year, currentDate.Month, day); // Сохраняем дату ячейки

            // Номер дня
            Label dayLabel = new Label();
            dayLabel.Text = day.ToString();
            dayLabel.Font = new Font("Arial", 12, FontStyle.Bold);
            dayLabel.TextAlign = ContentAlignment.MiddleCenter;
            dayLabel.Dock = DockStyle.Fill;
            dayLabel.BackColor = Color.Transparent;

            // Логика отображения для разных состояний
            UpdateDayCellAppearance(cell, dayLabel, isToday, isSelected, cellDate);

            cell.Controls.Add(dayLabel);

            // Обработчик клика
            cell.Click += (s, e) => SelectDate(cellDate);
            dayLabel.Click += (s, e) => SelectDate(cellDate);

            return cell;
        }

        private void UpdateDayCellAppearance(Panel cell, Label dayLabel, bool isToday, bool isSelected, DateTime cellDate)
        {
            // Сначала сбрасываем все стили
            cell.BorderStyle = BorderStyle.None;
            cell.BackColor = Color.White;

            bool isWeekend = cellDate.DayOfWeek == DayOfWeek.Saturday || cellDate.DayOfWeek == DayOfWeek.Sunday;

            if (isSelected && isToday)
            {
                // Если выбрана сегодняшняя дата - синий фон + синяя обводка
                cell.BackColor = Color.FromArgb(66, 133, 244);
                cell.BorderStyle = BorderStyle.FixedSingle;
                cell.ForeColor = Color.White;
                dayLabel.ForeColor = Color.White;
            }
            else if (isSelected)
            {
                // Только обводка для выбранной даты
                cell.BorderStyle = BorderStyle.FixedSingle;
                cell.BackColor = Color.White;
                dayLabel.ForeColor = Color.FromArgb(66, 133, 244);
            }
            else if (isToday)
            {
                // Синий фон для сегодняшней даты
                cell.BackColor = Color.FromArgb(66, 133, 244);
                dayLabel.ForeColor = Color.White;
            }
            else
            {
                // Обычная дата
                dayLabel.ForeColor = isWeekend ? Color.FromArgb(255, 68, 68) : Color.FromArgb(51, 51, 51);
            }
        }

        private void SelectDate(DateTime selectedCellDate)
        {
            DateTime previousSelectedDate = selectedDate;
            selectedDate = selectedCellDate;

            // Обновляем только нижнюю панель
            UpdateBottomPanel();

            // Обновляем только две ячейки: предыдущую выбранную и новую выбранную
            UpdateSingleDayCell(previousSelectedDate);
            UpdateSingleDayCell(selectedDate);
        }

        private void UpdateSingleDayCell(DateTime dateToUpdate)
        {
            // Обновляем только одну ячейку, если она принадлежит текущему месяцу
            if (dateToUpdate.Year == currentDate.Year && dateToUpdate.Month == currentDate.Month)
            {
                DateTime firstDayOfMonth = new DateTime(currentDate.Year, currentDate.Month, 1);
                int firstDayOfWeek = ((int)firstDayOfMonth.DayOfWeek + 6) % 7;
                int day = dateToUpdate.Day;

                // Вычисляем позицию ячейки
                int position = firstDayOfWeek + day - 1;
                int row = position / 7;
                int col = position % 7;

                if (row >= 0 && row < 6 && col >= 0 && col < 7 && dayCells[row, col] != null)
                {
                    Panel cell = dayCells[row, col];
                    Label dayLabel = (Label)cell.Controls[0];
                    DateTime cellDate = (DateTime)cell.Tag;

                    bool isToday = cellDate.Date == DateTime.Now.Date;
                    bool isSelected = cellDate.Date == selectedDate.Date;

                    // Обновляем внешний вид только этой ячейки
                    UpdateDayCellAppearance(cell, dayLabel, isToday, isSelected, cellDate);
                }
            }
        }

        private void PrevMonth()
        {
            currentDate = currentDate.AddMonths(-1);
            UpdateCalendar();
        }

        private void NextMonth()
        {
            currentDate = currentDate.AddMonths(1);
            UpdateCalendar();
        }

        private string GetMonthName(int month)
        {
            string[] months = {
                "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
            };
            return months[month - 1];
        }

        private void UpdateBottomPanel()
        {
            selectedDateLabel.Text = selectedDate.ToString("dd MMMM yyyy", new CultureInfo("ru-RU"));
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();
            this.ClientSize = new Size(382, 653);
            this.Name = "Form1";
            this.ResumeLayout(false);
        }
    }
}