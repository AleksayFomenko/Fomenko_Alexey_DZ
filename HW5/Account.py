from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt


class Account:
    _account_counter = 1000

    def __init__(self, account_holder, balance=0):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = balance
        Account._account_counter += 1
        self.holder = account_holder
        self.account_number = f"ACC-{self._account_counter}"
        self.operation_history = []

    def _add_operation(self, operation_type, amount, status):
        operation = {
            "operation_type": operation_type,
            "amount": amount,
            "date": datetime.now(),
            "balance": self._balance,
            "status": status,
        }
        self.operation_history.append(operation)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения счёта должна быть положительной")
        self._balance += amount
        self._add_operation("deposit", amount, "success")

    def withdrow(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия со счёта должна быть положительной")
        if self._balance - amount < 0:
            self._add_operation("withdrow", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdrow", amount, "success")

    def get_balance(self):
        return self._balance

    def get_history(self):
        return self.operation_history

    def plot_history(self):
        history_df = pd.DataFrame(self.operation_history)
        x = history_df["date"]
        y = history_df["balance"]
        fig, ax = plt.subplots()
        ax.plot(x, y)
        plt.axis()
        plt.title(f"Изменение баланса счёта {self.account_number} с течением времени")
        plt.xlabel("Время")
        plt.ylabel("Баланс")
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.show()
        return history_df

class CheckingAccount(Account): 
    def __init__(self):
        super().__init__()
        self.account_type = "CheckingAccount"

class SavingsAccount(Account): 
    def __init__(self):
        super().__init__()
        self.account_type = "SavingsAccount"
    
    def apply_interest(self, rate): # расчёт процентов на остаток
        pass


    def withdrow(self, amount): # нельзя снять больше 50 %
        if amount <= 0:
            raise ValueError("Сумма снятия со счёта должна быть положительной")
        if self._balance - amount < 0:
            self._add_operation("withdrow", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdrow", amount, "success")

ac1 = Account("pasha", 200)
ac2 = Account("hales", 3234)
ac1.withdrow(300)
ac1.deposit(600)
ac1.withdrow(300)
print(ac1.plot_history())
