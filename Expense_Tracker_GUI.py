import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import tkinter as tk
from expense_logic import ExpenseLogic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import calendar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.logic = ExpenseLogic()
        
        self.title("💰 Expense Tracker Pro")
        self.geometry("1200x750")
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Color scheme
        self.colors = {
            'primary': '#1f6aa5',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8',
            'dark': '#1a1a1a',
            'light': '#f8f9fa'
        }
        
        self.create_sidebar()
        self.create_main_frames()
        
        self.show_frame("dashboard")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
            self.destroy()

    def create_sidebar(self):
        """Create the sidebar navigation."""
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="💰 Expense\nTracker Pro", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "📊 Dashboard", 1),
            ("add_expense", "➕ Add Expense", 2),
            ("view_expenses", "📋 All Expenses", 3),
            ("current", "📅 This Month", 4),
            ("monthly", "📈 Compare Months", 5),
        ]
        
        for key, text, row in nav_items:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=lambda k=key: self.show_frame(k),
                width=180,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=row, column=0, padx=20, pady=8)
            self.nav_buttons[key] = btn
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="💾 Export Data",
            command=self.export_data,
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.export_btn.grid(row=6, column=0, padx=20, pady=8)
        
        # Separator
        separator = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30")
        separator.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance:", 
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
            width=180
        )
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(5, 10))
        self.appearance_mode_optionemenu.set("Dark")
        
        # UI Scaling
        self.scaling_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="UI Scaling:", 
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
            width=180
        )
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(5, 20))
        self.scaling_optionemenu.set("100%")

    def create_main_frames(self):
        """Create all main content frames."""
        # Dashboard Frame
        self.dashboard_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=0, 
            fg_color="transparent"
        )
        
        # Add Expense Frame
        self.add_expense_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=0, 
            fg_color="transparent"
        )
        self.setup_add_expense_ui()
        
        # View Expenses Frame
        self.view_expenses_frame = ctk.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="transparent"
        )
        self.setup_view_expenses_ui()

        # Current Month Frame
        self.current_frame = ctk.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color="transparent"
        )
        self.setup_current_month_ui()

        # Monthly Comparison Frame
        self.monthly_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=0, 
            fg_color="transparent"
        )
        self.setup_monthly_ui()

    def show_frame(self, name):
        """Show the specified frame and hide others."""
        # Hide all frames
        self.dashboard_frame.grid_forget()
        self.add_expense_frame.grid_forget()
        self.view_expenses_frame.grid_forget()
        self.current_frame.grid_forget()
        self.monthly_frame.grid_forget()
        
        # Update button states
        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.configure(fg_color=self.colors['primary'])
            else:
                btn.configure(fg_color=["#3a7ebf", "#1f538d"])
        
        # Show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.update_dashboard()
        elif name == "add_expense":
            self.add_expense_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "view_expenses":
            self.view_expenses_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.refresh_expense_list()
        elif name == "current":
            self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.refresh_current_list()
        elif name == "monthly":
            self.monthly_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.update_monthly_view()

    # --- Add Expense UI ---
    def setup_add_expense_ui(self):
        """Setup the Add Expense interface."""
        # Header
        header_frame = ctk.CTkFrame(self.add_expense_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title = ctk.CTkLabel(
            header_frame,
            text="➕ Add New Expense",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Track your spending by adding expense details below",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Form container
        form_frame = ctk.CTkFrame(self.add_expense_frame, fg_color="gray20", corner_radius=15)
        form_frame.pack(fill="both", expand=True, pady=20)
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(padx=40, pady=40, fill="both", expand=True)
        
        # Description
        desc_label = ctk.CTkLabel(
            fields_frame,
            text="Description *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 5))
        
        self.desc_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="e.g., Grocery shopping, Uber ride, Coffee",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.desc_entry.pack(fill="x", pady=(0, 20))
        
        # Amount
        amount_label = ctk.CTkLabel(
            fields_frame,
            text="Amount ($) *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        amount_label.pack(fill="x", pady=(0, 5))
        
        self.amount_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="0.00",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.amount_entry.pack(fill="x", pady=(0, 20))
        
        # Category
        cat_label = ctk.CTkLabel(
            fields_frame,
            text="Category *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        cat_label.pack(fill="x", pady=(0, 5))
        
        # Category dropdown with common categories
        self.category_var = tk.StringVar()
        self.type_entry = ctk.CTkComboBox(
            fields_frame,
            values=["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                    "Bills & Utilities", "Healthcare", "Education", "Travel", 
                    "Groceries", "Other"],
            variable=self.category_var,
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.type_entry.pack(fill="x", pady=(0, 20))
        self.type_entry.set("Food & Dining")
        
        # Date
        date_label = ctk.CTkLabel(
            fields_frame,
            text="Date *",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        date_label.pack(fill="x", pady=(0, 5))
        
        date_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 20))
        
        self.date_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="YYYY-MM-DD",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.date_entry.pack(side="left", fill="x", expand=True)
        self.date_entry.insert(0, str(datetime.date.today()))
        
        today_btn = ctk.CTkButton(
            date_frame,
            text="Today",
            command=lambda: self.date_entry.delete(0, "end") or self.date_entry.insert(0, str(datetime.date.today())),
            width=80,
            height=45,
            fg_color="gray30",
            hover_color="gray40"
        )
        today_btn.pack(side="left", padx=(10, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        self.add_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Expense",
            command=self.save_expense_action,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#228b22"
        )
        self.add_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_form,
            height=50,
            font=ctk.CTkFont(size=16),
            fg_color="gray30",
            hover_color="gray40"
        )
        clear_btn.pack(side="left", fill="x", expand=True)

    def clear_form(self):
        """Clear all form fields."""
        self.desc_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.type_entry.set("Food & Dining")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, str(datetime.date.today()))

    def save_expense_action(self):
        """Save the expense with validation."""
        desc = self.desc_entry.get()
        amount = self.amount_entry.get()
        cat = self.type_entry.get()
        date = self.date_entry.get()
        
        if not desc or not amount or not cat or not date:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        success, msg = self.logic.save_expense(desc, amount, cat, date)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.clear_form()
            # Update dashboard if it's visible
            if self.dashboard_frame.winfo_ismapped():
                self.update_dashboard()
        else:
            messagebox.showerror("Error", msg)

    # --- View Expenses UI ---
    def setup_view_expenses_ui(self):
        """Setup the View All Expenses interface."""
        # Header
        header_frame = ctk.CTkFrame(self.view_expenses_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📋 All Expenses",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Delete",
            command=self.delete_selected_action,
            width=120,
            height=40,
            fg_color=self.colors['danger'],
            hover_color="#c92a2a"
        )
        self.delete_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self.refresh_expense_list,
            width=120,
            height=40,
            fg_color=self.colors['info'],
            hover_color="#138496"
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(self.view_expenses_frame, fg_color="gray20", corner_radius=15)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configure style
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=35,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
            font=('Segoe UI', 11)
        )
        style.map('Treeview', background=[('selected', '#1f6aa5')])
        style.configure("Treeview.Heading",
                       background="#1f6aa5",
                       foreground="white",
                       relief="flat",
                       font=('Segoe UI', 12, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', '#1a5a8f')])
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Description", "Category", "Amount", "Date"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="browse"
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount ($)")
        self.tree.heading("Date", text="Date")
        
        # Column widths
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Description", width=300)
        self.tree.column("Category", width=150)
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Date", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Total label
        self.total_expenses_label = ctk.CTkLabel(
            self.view_expenses_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.total_expenses_label.pack(pady=(0, 20))

    def refresh_expense_list(self):
        """Refresh the expense list in the treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load and display expenses
        expenses = self.logic.load_expenses()
        total = 0
        
        for exp in expenses:
            self.tree.insert("", "end", values=(
                exp["Id"],
                exp["Description"],
                exp["Expense_Type"],
                f"${float(exp['Amount']):.2f}",
                exp["Date"]
            ))
            total += float(exp["Amount"])
        
        self.total_expenses_label.configure(text=f"Total: ${total:.2f} ({len(expenses)} expenses)")

    def delete_selected_action(self):
        """Delete the selected expense."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?\nThis action cannot be undone."
        )
        
        if confirm:
            item = self.tree.item(selected[0])
            exp_id = item['values'][0]
            success, msg = self.logic.delete_expense(exp_id)
            
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_expense_list()
                if self.dashboard_frame.winfo_ismapped():
                    self.update_dashboard()
            else:
                messagebox.showerror("Error", msg)

    # --- Current Month UI ---
    def setup_current_month_ui(self):
        """Setup the Current Month Expenses interface."""
        # Header
        header_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📅 This Month's Expenses",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.refresh_current_list,
            width=120,
            height=40,
            fg_color=self.colors['info'],
            hover_color="#138496"
        )
        refresh_btn.pack(side="right")
        
        # Treeview frame
        tree_frame = ctk.CTkFrame(self.current_frame, fg_color="gray20", corner_radius=15)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbars
        tree_scroll_y2 = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y2.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Treeview
        self.tree_current = ttk.Treeview(
            tree_frame,
            columns=("ID", "Description", "Category", "Amount", "Date"),
            show="headings",
            yscrollcommand=tree_scroll_y2.set,
            selectmode="browse"
        )
        
        tree_scroll_y2.config(command=self.tree_current.yview)
        
        # Column headings
        self.tree_current.heading("ID", text="ID")
        self.tree_current.heading("Description", text="Description")
        self.tree_current.heading("Category", text="Category")
        self.tree_current.heading("Amount", text="Amount ($)")
        self.tree_current.heading("Date", text="Date")
        
        # Column widths
        self.tree_current.column("ID", width=50, anchor="center")
        self.tree_current.column("Description", width=300)
        self.tree_current.column("Category", width=150)
        self.tree_current.column("Amount", width=100, anchor="e")
        self.tree_current.column("Date", width=120, anchor="center")
        
        self.tree_current.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self.current_frame, fg_color="gray20", corner_radius=15)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.current_total_label = ctk.CTkLabel(
            stats_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.current_total_label.pack(pady=20)

    def refresh_current_list(self):
        """Refresh current month's expense list."""
        # Clear existing items
        for item in self.tree_current.get_children():
            self.tree_current.delete(item)
        
        # Load and display current month expenses
        expenses = self.logic.load_current_month_expenses()
        total = 0
        
        for exp in expenses:
            self.tree_current.insert("", "end", values=(
                exp["Id"],
                exp["Description"],
                exp["Expense_Type"],
                f"${float(exp['Amount']):.2f}",
                exp["Date"]
            ))
            total += float(exp["Amount"])
        
        month_name = calendar.month_name[datetime.date.today().month]
        self.current_total_label.configure(
            text=f"{month_name} Total: ${total:.2f} ({len(expenses)} expenses)"
        )

    # --- Monthly Comparison UI ---
    def setup_monthly_ui(self):
        """Setup the Monthly Comparison interface."""
        # Header
        header_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📈 Monthly Comparison",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Compare your spending across different months",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Stats cards frame
        cards_frame = ctk.CTkFrame(self.monthly_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=20)
        
        # Current month card
        current_card = ctk.CTkFrame(cards_frame, fg_color="gray20", corner_radius=15)
        current_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        current_label = ctk.CTkLabel(
            current_card,
            text="Current Month",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        current_label.pack(pady=(20, 5))
        
        self.monthly_total_lbl = ctk.CTkLabel(
            current_card,
            text="$0.00",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.monthly_total_lbl.pack(pady=(0, 20))
        
        # Previous month card
        prev_card = ctk.CTkFrame(cards_frame, fg_color="gray20", corner_radius=15)
        prev_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        prev_label = ctk.CTkLabel(
            prev_card,
            text="Previous Month",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        prev_label.pack(pady=(20, 5))
        
        self.monthly_prev_lbl = ctk.CTkLabel(
            prev_card,
            text="$0.00",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.monthly_prev_lbl.pack(pady=(0, 20))
        
        # Change card
        change_card = ctk.CTkFrame(cards_frame, fg_color="gray20", corner_radius=15)
        change_card.pack(side="left", fill="both", expand=True)
        
        change_label = ctk.CTkLabel(
            change_card,
            text="Change",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        change_label.pack(pady=(20, 5))
        
        self.monthly_change_lbl = ctk.CTkLabel(
            change_card,
            text="0%",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.monthly_change_lbl.pack(pady=(0, 20))
        
        # Chart frame
        chart_container = ctk.CTkFrame(self.monthly_frame, fg_color="gray20", corner_radius=15)
        chart_container.pack(fill="both", expand=True, pady=20)
        
        chart_title = ctk.CTkLabel(
            chart_container,
            text="Monthly Totals (All Time)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chart_title.pack(pady=(20, 10))
        
        self.monthly_chart_frame = ctk.CTkFrame(chart_container, fg_color="transparent")
        self.monthly_chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def update_monthly_view(self):
        """Update the monthly comparison view."""
        # Clear chart area
        for widget in self.monthly_chart_frame.winfo_children():
            widget.destroy()

        # Get comparison data
        comp = self.logic.compare_months_master()
        
        # Update stats
        self.monthly_total_lbl.configure(text=f"${comp['current_total']:.2f}")
        
        if comp['prev_exists'] or comp['previous_total'] > 0:
            self.monthly_prev_lbl.configure(text=f"${comp['previous_total']:.2f}")
            
            if comp['percent_change'] is not None:
                sign = "+" if comp['difference'] > 0 else ""
                pct = comp['percent_change']
                
                if comp['difference'] > 0:
                    change_text = f"{sign}{pct:.1f}% 📈"
                    change_color = self.colors['danger']
                elif comp['difference'] < 0:
                    change_text = f"{pct:.1f}% 📉"
                    change_color = self.colors['success']
                else:
                    change_text = "0% ➡️"
                    change_color = "gray60"
                
                self.monthly_change_lbl.configure(text=change_text, text_color=change_color)
            else:
                self.monthly_change_lbl.configure(text="N/A", text_color="gray60")
        else:
            self.monthly_prev_lbl.configure(text="No data")
            self.monthly_change_lbl.configure(text="N/A", text_color="gray60")

        # Create chart
        monthly_totals = self.logic.get_all_monthly_totals_from_master()
        
        if monthly_totals:
            # Sort months chronologically
            month_map = {name: i for i, name in enumerate(calendar.month_name) if name}
            sorted_months = sorted([m for m in monthly_totals.keys()], key=lambda x: month_map.get(x, 0))
            totals = [monthly_totals[m] for m in sorted_months]
            
            # Create figure
            fig = Figure(figsize=(10, 4), dpi=100)
            fig.patch.set_facecolor('#2a2d2e')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2a2d2e')
            
            # Highlight current month
            current = calendar.month_name[datetime.date.today().month]
            colors = [self.colors['warning'] if m == current else self.colors['primary'] for m in sorted_months]
            
            bars = ax.bar(sorted_months, totals, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'${height:.0f}',
                       ha='center', va='bottom', color='white', fontsize=9)
            
            ax.tick_params(axis='x', colors='white', rotation=45, labelsize=10)
            ax.tick_params(axis='y', colors='white', labelsize=10)
            ax.set_ylabel('Amount ($)', color='white', fontsize=11)
            ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('white')
            ax.spines['bottom'].set_color('white')
            
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=self.monthly_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            no_data_label = ctk.CTkLabel(
                self.monthly_chart_frame,
                text="No data available yet\nStart adding expenses to see monthly trends!",
                font=ctk.CTkFont(size=16),
                text_color="gray60"
            )
            no_data_label.pack(expand=True)

    # --- Dashboard UI ---
    def update_dashboard(self):
        """Update the dashboard view."""
        # Clear existing widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        data = self.logic.get_summary_data()
        
        if not data:
            # No data available
            empty_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
            empty_frame.pack(expand=True)
            
            icon = ctk.CTkLabel(
                empty_frame,
                text="📊",
                font=ctk.CTkFont(size=80)
            )
            icon.pack(pady=20)
            
            no_data_label = ctk.CTkLabel(
                empty_frame,
                text="No Expenses This Month",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            no_data_label.pack()
            
            hint_label = ctk.CTkLabel(
                empty_frame,
                text="Click 'Add Expense' to start tracking your spending",
                font=ctk.CTkFont(size=14),
                text_color="gray60"
            )
            hint_label.pack(pady=10)
            
            add_btn = ctk.CTkButton(
                empty_frame,
                text="➕ Add Your First Expense",
                command=lambda: self.show_frame("add_expense"),
                height=50,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=self.colors['success'],
                hover_color="#228b22"
            )
            add_btn.pack(pady=20)
            
            return

        # Header
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")
        
        month_name = calendar.month_name[datetime.date.today().month]
        month_label = ctk.CTkLabel(
            header_frame,
            text=f"{month_name} {datetime.date.today().year}",
            font=ctk.CTkFont(size=16),
            text_color="gray60"
        )
        month_label.pack(side="left", padx=20)

        # Stats Cards
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        # Total card
        total_card = ctk.CTkFrame(stats_frame, fg_color="gray20", corner_radius=15)
        total_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        total_title = ctk.CTkLabel(
            total_card,
            text="💰 Total Spent",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        total_title.pack(pady=(20, 5))
        
        total_value = ctk.CTkLabel(
            total_card,
            text=f"${data['total_amount']:.2f}",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        total_value.pack(pady=(0, 20))
        
        # Count card
        count_card = ctk.CTkFrame(stats_frame, fg_color="gray20", corner_radius=15)
        count_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        count_title = ctk.CTkLabel(
            count_card,
            text="📝 Transactions",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        count_title.pack(pady=(20, 5))
        
        count_value = ctk.CTkLabel(
            count_card,
            text=str(data['count']),
            font=ctk.CTkFont(size=32, weight="bold")
        )
        count_value.pack(pady=(0, 20))
        
        # Average card
        avg_card = ctk.CTkFrame(stats_frame, fg_color="gray20", corner_radius=15)
        avg_card.pack(side="left", fill="both", expand=True)
        
        avg_title = ctk.CTkLabel(
            avg_card,
            text="📊 Average",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        avg_title.pack(pady=(20, 5))
        
        avg_value = ctk.CTkLabel(
            avg_card,
            text=f"${data['average']:.2f}",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        avg_value.pack(pady=(0, 20))

        # Charts Container
        charts_container = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        charts_container.pack(fill="both", expand=True, pady=20)
        
        # Category Pie Chart
        if data["expense_by_type"]:
            pie_frame = ctk.CTkFrame(charts_container, fg_color="gray20", corner_radius=15)
            pie_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            pie_title = ctk.CTkLabel(
                pie_frame,
                text="Expenses by Category",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            pie_title.pack(pady=(15, 5))
            
            pie_chart_frame = ctk.CTkFrame(pie_frame, fg_color="transparent")
            pie_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            fig1 = Figure(figsize=(5, 4), dpi=100)
            fig1.patch.set_facecolor('#2a2d2e')
            ax1 = fig1.add_subplot(111)
            ax1.set_facecolor('#2a2d2e')
            
            types = list(data["expense_by_type"].keys())
            amounts = list(data["expense_by_type"].values())
            
            colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                         '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            
            wedges, texts, autotexts = ax1.pie(
                amounts, 
                labels=types, 
                autopct='%1.1f%%', 
                startangle=90,
                colors=colors_pie[:len(amounts)],
                textprops={'color': "white", 'fontsize': 10}
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
            
            canvas1 = FigureCanvasTkAgg(fig1, master=pie_chart_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="both", expand=True)
        
        # Daily Bar Chart
        if data["expense_by_date"]:
            bar_frame = ctk.CTkFrame(charts_container, fg_color="gray20", corner_radius=15)
            bar_frame.pack(side="left", fill="both", expand=True)
            
            bar_title = ctk.CTkLabel(
                bar_frame,
                text="Daily Expenses",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            bar_title.pack(pady=(15, 5))
            
            bar_chart_frame = ctk.CTkFrame(bar_frame, fg_color="transparent")
            bar_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            fig2 = Figure(figsize=(5, 4), dpi=100)
            fig2.patch.set_facecolor('#2a2d2e')
            ax2 = fig2.add_subplot(111)
            ax2.set_facecolor('#2a2d2e')
            
            dates = list(data["expense_by_date"].keys())
            daily_amounts = list(data["expense_by_date"].values())
            
            # Sort by date
            sorted_pairs = sorted(zip(dates, daily_amounts))
            if sorted_pairs:
                dates, daily_amounts = zip(*sorted_pairs)
            
            # Format dates for display (show only day)
            display_dates = [d.split('-')[-1] for d in dates]
            
            bars = ax2.bar(display_dates, daily_amounts, color=self.colors['primary'], alpha=0.8)
            
            ax2.tick_params(axis='x', colors='white', rotation=45, labelsize=9)
            ax2.tick_params(axis='y', colors='white', labelsize=9)
            ax2.set_ylabel('Amount ($)', color='white', fontsize=10)
            ax2.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Remove top and right spines
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('white')
            ax2.spines['bottom'].set_color('white')
            
            fig2.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, master=bar_chart_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True)

    def export_data(self):
        """Export data to CSV file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"expenses_export_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            success, msg = self.logic.export_to_csv(filename)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode)
        # Refresh current view
        current_frame = None
        for name, frame in [
            ("dashboard", self.dashboard_frame),
            ("add_expense", self.add_expense_frame),
            ("view_expenses", self.view_expenses_frame),
            ("current", self.current_frame),
            ("monthly", self.monthly_frame)
        ]:
            if frame.winfo_ismapped():
                current_frame = name
                break
        
        if current_frame:
            self.show_frame(current_frame)

    def change_scaling_event(self, new_scaling: str):
        """Change UI scaling."""
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
