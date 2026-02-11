# 🚀 Quick Start Guide - Expense Tracker Pro

## Installation (2 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python Expense_Tracker_GUI.py
```

That's it! The app will launch automatically.

## First Time Setup

### Your First Expense
1. Click **"➕ Add Expense"** in the sidebar
2. Enter:
   - Description: "Coffee"
   - Amount: "4.50"
   - Category: "Food & Dining"
   - Date: (leave as today)
3. Click **"💾 Save Expense"**
4. Success! ✅

### Explore the Dashboard
1. Click **"📊 Dashboard"** in sidebar
2. You'll see:
   - Total spending this month
   - Number of transactions
   - Average expense amount
   - Visual charts of your spending

## Common Tasks

### Add Multiple Expenses Quickly
1. Go to Add Expense
2. Fill in details
3. Click Save
4. Form clears automatically
5. Repeat!

### View All Your Expenses
1. Click **"📋 All Expenses"**
2. See complete history in table format
3. Sort by clicking column headers
4. Delete unwanted entries

### Check This Month's Spending
1. Click **"📅 This Month"**
2. See only current month expenses
3. View monthly total at bottom

### Compare Months
1. Click **"📈 Compare Months"**
2. See current vs previous month
3. View percentage change
4. Check historical bar chart

### Export Your Data
1. Click **"💾 Export Data"** in sidebar
2. Choose save location
3. File saves as CSV
4. Open in Excel/Google Sheets

## Keyboard Shortcuts

- **Tab**: Move between fields
- **Enter**: Submit form (when in Add Expense)
- **Escape**: Cancel dialogs

## Pro Tips 💡

1. **Use Categories Consistently**: Makes analytics more meaningful
2. **Daily Tracking**: Add expenses daily for best results
3. **Regular Exports**: Backup your data monthly
4. **Check Comparisons**: Review monthly trends to improve spending
5. **Customize Appearance**: Find your preferred theme in sidebar

## Troubleshooting

### App Won't Start?
```bash
# Reinstall dependencies
pip install --upgrade customtkinter matplotlib
```

### Charts Not Showing?
- Check matplotlib is installed: `pip list | grep matplotlib`
- Try: `pip install --upgrade matplotlib`

### Data Not Saving?
- Check you have write permissions in the app folder
- Look for `all_expenses.csv` in the same folder as the app

## Need Help?

- Read the full **README.md** for detailed documentation
- Check file permissions in your directory
- Ensure Python 3.8+ is installed: `python --version`

---

**You're all set! Start tracking your expenses! 💰**
