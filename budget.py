import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox

class BudgetTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.income = 0
        self.expenses = []
        self.categories = []
        self.budget_limit = 0

    def initUI(self):
        self.setWindowTitle('Budget Tracker')
        layout = QVBoxLayout()

        self.income_label = QLabel('Enter your Income:')
        layout.addWidget(self.income_label)

        self.income_input = QLineEdit()
        layout.addWidget(self.income_input)

        self.budget_limit_label = QLabel('Set Budget Limit:')
        layout.addWidget(self.budget_limit_label)

        self.budget_limit_input = QLineEdit()
        layout.addWidget(self.budget_limit_input)

        self.expense_label = QLabel('Select Expense Category:')
        layout.addWidget(self.expense_label)

        self.category_input = QComboBox()
        self.category_input.addItems(['Food', 'Transport', 'Entertainment', 'Utilities', 'Others'])
        layout.addWidget(self.category_input)

        self.expense_amount_label = QLabel('Enter your Expense Amount:')
        layout.addWidget(self.expense_amount_label)

        self.expense_input = QLineEdit()
        layout.addWidget(self.expense_input)

        self.submit_button = QPushButton('Add Expense')
        self.submit_button.clicked.connect(self.add_expense)
        layout.addWidget(self.submit_button)

        self.plot_button = QPushButton('Show Expenses Graph')
        self.plot_button.clicked.connect(self.plot_expenses)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def add_expense(self):
        try:
            expense = float(self.expense_input.text())
            category = self.category_input.currentText()

            if self.income == 0:
                self.income = float(self.income_input.text())

            if self.budget_limit == 0:
                self.budget_limit = float(self.budget_limit_input.text())

            total_expenses = sum(self.expenses) + expense

            if total_expenses > self.budget_limit:
                adjusted_expense = self.budget_limit - sum(self.expenses)
                if adjusted_expense > 0:
                    self.expenses.append(adjusted_expense)
                    self.categories.append(category)
                    QMessageBox.warning(self, 'Expense Adjusted', f'Your total expenses exceeded your budget limit.\nThe last expense was adjusted to Rs{adjusted_expense} to stay within your budget.')
                else:
                    QMessageBox.warning(self, 'Budget Limit Reached', 'Your expenses have reached the budget limit. No more expenses can be added.')
            else:
                self.expenses.append(expense)
                self.categories.append(category)

            self.expense_input.clear()

        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid number.')

    def plot_expenses(self):
        df = pd.DataFrame({'Expenses': self.expenses, 'Categories': self.categories})
        df.index += 1

        plt.figure(figsize=(10, 5))

        for category in df['Categories'].unique():
            plt.plot(df[df['Categories'] == category].index, df[df['Categories'] == category]['Expenses'], marker='o', label=category)

        plt.axhline(y=self.income, color='r', linestyle='--', label='Income')
        plt.axhline(y=self.budget_limit, color='g', linestyle='-', label='Budget Limit')

        remaining_budget = [self.budget_limit - sum(self.expenses[:i]) for i in range(1, len(self.expenses)+1)]
        plt.plot(df.index, remaining_budget, color='b', linestyle='-', marker='x', label='Remaining Budget')

        plt.legend()
        plt.title('Historic Expense Tracking by Category')
        plt.xlabel('Expense Entry')
        plt.ylabel('Amount (Rs)')
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = BudgetTracker()
    tracker.resize(400, 300)
    tracker.show()
    sys.exit(app.exec_())