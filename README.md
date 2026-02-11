# 💰 Expense Tracker Pro

A modern, user-friendly desktop application for tracking personal expenses with beautiful visualizations and comprehensive analytics.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 📊 Dashboard
- **Real-time Statistics**: View total expenses, transaction count, and average spending at a glance
- **Visual Analytics**: 
  - Pie chart showing expense distribution by category
  - Bar chart displaying daily spending patterns
- **Monthly Focus**: Dashboard shows current month's data by default

### ➕ Add Expense
- **Intuitive Form**: Clean, modern interface for adding new expenses
- **Smart Categories**: Pre-populated category dropdown with common expense types:
  - Food & Dining
  - Transportation
  - Shopping
  - Entertainment
  - Bills & Utilities
  - Healthcare
  - Education
  - Travel
  - Groceries
  - Other
- **Auto-date**: Automatically fills today's date with easy "Today" button
- **Input Validation**: Ensures data integrity with comprehensive validation

### 📋 View All Expenses
- **Sortable Table**: View all expenses in a clean, organized table
- **Quick Actions**: 
  - Delete expenses with confirmation
  - Refresh data instantly
- **Running Total**: See total spending across all time

### 📅 This Month
- **Current Month Focus**: Filtered view of current month's expenses
- **Monthly Total**: Quick summary of month-to-date spending

### 📈 Monthly Comparison
- **Trend Analysis**: Compare current month with previous month
- **Visual Indicators**: 
  - 📈 Upward trend (increased spending)
  - 📉 Downward trend (decreased spending)
  - ➡️ No change
- **Historical Chart**: Bar chart showing spending trends across all months
- **Percentage Change**: See exactly how much your spending has changed

### 💾 Data Management
- **Export Functionality**: Export all expenses to CSV for backup or analysis
- **Auto-backup**: Expenses are automatically backed up to monthly files
- **Master Database**: Central `all_expenses.csv` file maintains all data

### 🎨 Customization
- **Appearance Modes**: 
  - Dark Mode (default)
  - Light Mode
  - System (follows OS preference)
- **UI Scaling**: Adjust interface size (80% - 120%)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download** the repository

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

Simply run the main GUI file:
```bash
python Expense_Tracker_GUI.py
```

## 📁 File Structure

```
expense-tracker/
├── Expense_Tracker_GUI.py    # Main application file
├── expense_logic.py           # Business logic and data management
├── requirements.txt           # Python dependencies
├── all_expenses.csv          # Master database (created automatically)
└── [Month].csv               # Monthly backup files (created automatically)
```

## 💾 Data Storage

### Master File
- **Location**: `all_expenses.csv`
- **Purpose**: Central database containing all expenses
- **Format**: CSV with columns: Id, Description, Expense_Type, Amount, Date

### Monthly Backups
- **Location**: `[MonthName].csv` (e.g., `January.csv`, `February.csv`)
- **Purpose**: Monthly backup files for additional safety
- **Auto-created**: Generated automatically when adding expenses

### Data Migration
The app automatically migrates data from old monthly files to the new master file system on first run.

## 🛠️ Key Improvements Over Original

### Bug Fixes
1. ✅ Fixed missing `sync_missing_from_previous_months()` method
2. ✅ Added proper error handling throughout
3. ✅ Fixed chart rendering issues
4. ✅ Improved data validation

### UI Enhancements
1. 🎨 Modern, clean interface with CustomTkinter
2. 📊 Better data visualization with improved charts
3. 🔄 Intuitive navigation with emoji icons
4. 📱 Responsive design with proper scaling
5. 🎯 Card-based statistics display
6. 🌈 Consistent color scheme throughout
7. ✨ Smooth transitions and animations

### Functionality Improvements
1. 📝 Category dropdown with common options
2. ✅ Comprehensive input validation
3. 🔒 Confirmation dialogs for destructive actions
4. 💾 Export functionality for data backup
5. 📊 Enhanced analytics (average spending, better comparisons)
6. 🔄 Smart refresh and update mechanisms
7. 📅 "Today" button for quick date selection

### User Experience
1. 🎯 Clear visual hierarchy
2. 📖 Helpful empty states with guidance
3. ⚠️ Better error messages
4. ✅ Success feedback for actions
5. 🖱️ Improved button placement and sizing
6. 🎨 Professional color coding (success = green, danger = red, etc.)

## 📊 Usage Tips

### Adding Your First Expense
1. Click "➕ Add Expense" in the sidebar
2. Fill in the description (e.g., "Lunch at cafe")
3. Enter the amount (e.g., "15.50")
4. Select a category from the dropdown
5. Verify/adjust the date
6. Click "💾 Save Expense"

### Viewing Analytics
- **Dashboard**: Shows current month's overview with charts
- **This Month**: Detailed list of current month expenses
- **Compare Months**: See how your spending trends over time

### Managing Expenses
- **Delete**: Select an expense in "All Expenses" view and click "🗑️ Delete"
- **Export**: Click "💾 Export Data" in sidebar to save a backup

### Customization
- Change appearance mode in sidebar (Dark/Light/System)
- Adjust UI scaling for comfort (80% - 120%)

## 🔧 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Install dependencies: `pip install -r requirements.txt`

### Data not appearing
- Check if `all_expenses.csv` exists in the application directory
- Try adding a new expense to initialize the database

### Charts not rendering
- Ensure matplotlib is properly installed
- Try reinstalling: `pip install --upgrade matplotlib`

## 📝 Data Format

### CSV Structure
```csv
Id,Description,Expense_Type,Amount,Date
1,Grocery Shopping,Food & Dining,45.50,2025-02-11
2,Uber Ride,Transportation,15.00,2025-02-11
```

### Date Format
All dates use ISO format: `YYYY-MM-DD` (e.g., 2025-02-11)

## 🔐 Privacy & Security

- **Local Storage**: All data is stored locally on your computer
- **No Cloud**: No data is sent to external servers
- **Backup Recommended**: Regular exports ensure data safety

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest features
- Submit improvements

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Charts powered by [Matplotlib](https://matplotlib.org/)

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the Usage Tips
3. Ensure all dependencies are installed

---

**Made with ❤️ for better financial tracking**

*Version: 2.0*
*Last Updated: February 2025*
