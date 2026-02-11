import csv
import os
import datetime
import calendar

class ExpenseLogic:
    def __init__(self):
        self.master_filename = "all_expenses.csv"
        self.ensure_master_exists()
        self.migrate_if_needed()

    def ensure_master_exists(self):
        """Create master file if it doesn't exist."""
        if not os.path.exists(self.master_filename):
            with open(self.master_filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                writer.writeheader()

    def migrate_if_needed(self):
        """
        If master file is empty but monthly files exist, populate master from them.
        This runs once to transition the user.
        """
        if os.path.exists(self.master_filename) and os.path.getsize(self.master_filename) > 50:
            return  # Assume populated if > 50 bytes (header is ~45)

        all_rows = []
        seen_keys = set()
        
        # Read from all potential month files
        for m in range(1, 13):
            mname = calendar.month_name[m]
            fname = f"{mname}.csv"
            if os.path.exists(fname):
                try:
                    with open(fname, "r", newline="") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            key = self._row_key(row)
                            if key not in seen_keys:
                                all_rows.append(row)
                                seen_keys.add(key)
                except Exception as e:
                    print(f"Error reading {fname}: {e}")

        if all_rows:
            # Sort by date
            all_rows.sort(key=lambda x: x.get("Date", ""))
            # Re-assign IDs sequentially
            for i, row in enumerate(all_rows):
                row["Id"] = i + 1
            
            self._rewrite_file(all_rows, self.master_filename)

    def load_expenses(self):
        """Load ALL expenses from master file."""
        if os.path.exists(self.master_filename):
            try:
                with open(self.master_filename, "r", newline="") as file:
                    reader = csv.DictReader(file)
                    return list(reader)
            except Exception as e:
                print(f"Error loading expenses: {e}")
                return []
        return []

    def load_current_month_expenses(self):
        """Filter expenses for current month from master file."""
        all_exp = self.load_expenses()
        today = datetime.date.today()
        
        filtered = []
        for exp in all_exp:
            try:
                edate = exp["Date"]
                dt = datetime.datetime.strptime(edate, "%Y-%m-%d")
                if dt.month == today.month and dt.year == today.year:
                    filtered.append(exp)
            except ValueError:
                pass  # Skip invalid dates
        return filtered

    def validate_date(self, date_string):
        """Validate date format."""
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True, "Valid date"
        except ValueError:
            return False, "Invalid date format. Please use YYYY-MM-DD"

    def validate_amount(self, amount_string):
        """Validate amount."""
        try:
            amount = float(amount_string)
            if amount <= 0:
                return False, "Amount must be greater than 0"
            return True, amount
        except ValueError:
            return False, "Amount must be a valid number"

    def save_expense(self, description, amount, expense_type, date):
        """Save a new expense to the master file and monthly backup."""
        # Validate inputs
        if not description.strip():
            return False, "Description cannot be empty"
        
        if not expense_type.strip():
            return False, "Category cannot be empty"
        
        valid_date, msg = self.validate_date(date)
        if not valid_date:
            return False, msg
        
        valid_amount, amount_value = self.validate_amount(amount)
        if not valid_amount:
            return False, amount_value
        
        expenses = self.load_expenses()
        
        # Calculate new ID
        max_id = 0
        if expenses:
            try:
                max_id = max(int(row["Id"]) for row in expenses)
            except ValueError:
                max_id = len(expenses) 
        
        new_id = max_id + 1
        
        new_expense = {
            "Id": new_id,
            "Description": description.strip(),
            "Expense_Type": expense_type.strip(),
            "Amount": f"{amount_value:.2f}",
            "Date": date
        }
        
        try:
            # 1. Append to Master
            with open(self.master_filename, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                if os.path.getsize(self.master_filename) == 0:
                    writer.writeheader()
                writer.writerow(new_expense)

            # 2. Append to Monthly Backup
            dt = datetime.datetime.strptime(date, "%Y-%m-%d")
            month_file = f"{calendar.month_name[dt.month]}.csv"
            
            file_exists = os.path.exists(month_file)
            with open(month_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                if not file_exists or os.path.getsize(month_file) == 0:
                    writer.writeheader()
                writer.writerow(new_expense)
                
            return True, "Expense added successfully"
        except Exception as e:
            return False, f"Error saving expense: {str(e)}"

    def delete_expense(self, expense_id):
        """Delete an expense from the master file."""
        try:
            expenses = self.load_expenses()
            initial_count = len(expenses)
            expenses = [exp for exp in expenses if str(exp["Id"]) != str(expense_id)]
            
            if len(expenses) < initial_count:
                self._rewrite_file(expenses, self.master_filename)
                return True, f"Expense ID {expense_id} deleted successfully"
            return False, "Expense ID not found"
        except Exception as e:
            return False, f"Error deleting expense: {str(e)}"

    def update_expense(self, expense_id, new_data):
        """Update an existing expense."""
        try:
            expenses = self.load_expenses()
            updated = False
            for exp in expenses:
                if str(exp["Id"]) == str(expense_id):
                    exp.update(new_data)
                    updated = True
                    break
            
            if updated:
                self._rewrite_file(expenses, self.master_filename)
                return True, "Expense updated successfully"
            return False, "Expense ID not found"
        except Exception as e:
            return False, f"Error updating expense: {str(e)}"

    def _rewrite_file(self, expenses, filename):
        """Rewrite entire CSV file with new data."""
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
            writer.writeheader()
            writer.writerows(expenses)

    def get_summary_data(self):
        """Get summary statistics for current month."""
        expenses = self.load_current_month_expenses()
        if not expenses:
            return None
            
        amounts = [float(row["Amount"]) for row in expenses]
        total_amount = sum(amounts)
        
        # Breakdown by Type
        expense_by_type = {}
        for row in expenses:
            exp_type = row["Expense_Type"]
            amount = float(row["Amount"])
            expense_by_type[exp_type] = expense_by_type.get(exp_type, 0) + amount
            
        # Group by Date
        expense_by_date = {} 
        for row in expenses:
            date_str = row["Date"]
            amount = float(row["Amount"])
            expense_by_date[date_str] = expense_by_date.get(date_str, 0) + amount

        return {
            "total_amount": total_amount,
            "expense_by_type": expense_by_type,
            "expense_by_date": expense_by_date,
            "count": len(expenses),
            "average": total_amount / len(expenses) if expenses else 0
        }

    def get_all_time_summary(self):
        """Get summary statistics for all time."""
        expenses = self.load_expenses()
        if not expenses:
            return None
            
        amounts = [float(row["Amount"]) for row in expenses]
        total_amount = sum(amounts)
        
        expense_by_type = {}
        for row in expenses:
            exp_type = row["Expense_Type"]
            amount = float(row["Amount"])
            expense_by_type[exp_type] = expense_by_type.get(exp_type, 0) + amount

        return {
            "total_amount": total_amount,
            "expense_by_type": expense_by_type,
            "count": len(expenses),
            "average": total_amount / len(expenses) if expenses else 0
        }

    def _row_key(self, row):
        """Create a normalized key for a row to detect duplicates."""
        desc = str(row.get("Description", "")).strip()
        etype = str(row.get("Expense_Type", "")).strip()
        try:
            amt = f"{float(row.get('Amount', 0)):.2f}"
        except Exception:
            amt = str(row.get("Amount", "")).strip()
        date = str(row.get("Date", "")).strip()
        return (desc, etype, amt, date)

    def get_all_monthly_totals_from_master(self):
        """Calculate totals per month from master file."""
        expenses = self.load_expenses()
        totals = {}
        
        for row in expenses:
            try:
                date_str = row["Date"]
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                mname = calendar.month_name[dt.month]
                amt = float(row["Amount"])
                totals[mname] = totals.get(mname, 0) + amt
            except ValueError:
                pass
                
        return totals

    def compare_months_master(self):
        """Compare current month vs previous month using Master Data."""
        totals = self.get_all_monthly_totals_from_master()
        
        today = datetime.date.today()
        curr_month_name = calendar.month_name[today.month]
        
        prev_date = today.replace(day=1) - datetime.timedelta(days=1)
        prev_month_name = calendar.month_name[prev_date.month]
        
        current_total = totals.get(curr_month_name, 0.0)
        previous_total = totals.get(prev_month_name, 0.0)
        prev_exists = prev_month_name in totals
        
        difference = current_total - previous_total
        percent_change = None
        if previous_total != 0:
            percent_change = (difference / previous_total) * 100
            
        status = "same"
        if not prev_exists and previous_total == 0:
            status = "no_prev_data"
        elif difference > 0:
            status = "increase"
        elif difference < 0:
            status = "decrease"
            
        return {
            "current_total": current_total,
            "previous_total": previous_total,
            "difference": difference,
            "percent_change": percent_change,
            "prev_month_name": prev_month_name,
            "curr_month_name": curr_month_name,
            "prev_exists": prev_exists,
            "status": status
        }

    def export_to_csv(self, filename=None):
        """Export all expenses to a CSV file."""
        if filename is None:
            filename = f"expenses_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            expenses = self.load_expenses()
            if not expenses:
                return False, "No expenses to export"
            
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Id", "Description", "Expense_Type", "Amount", "Date"])
                writer.writeheader()
                writer.writerows(expenses)
            
            return True, f"Exported {len(expenses)} expenses to {filename}"
        except Exception as e:
            return False, f"Error exporting: {str(e)}"
