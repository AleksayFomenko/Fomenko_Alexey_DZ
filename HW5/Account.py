from datetime import datetime
import pandas as pd
from matplotlib import dates as mdates, pyplot as plt
import re


class Account:  # Базовый класс - банковский счёт
    _account_counter = 1000

    def __init__(self, account_holder, balance=0):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        if not re.fullmatch(r"^[A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+", account_holder):
            raise ValueError("Неверный формат имени владельца счёта")
        self._balance = balance
        Account._account_counter += 1
        self.holder = account_holder
        self.account_number = f"ACC-{self._account_counter}"
        self.operation_history = []

    def _add_operation(
        self, operation_type, amount, status
    ):  # Метод для добавления операций в историю
        operation = {
            "operation_type": operation_type,
            "amount": amount,
            "date": datetime.now(),
            "balance": self._balance,
            "status": status,
        }
        self.operation_history.append(operation)

    def deposit(self, amount):  # Метод пополнения счёта
        if amount <= 0:
            raise ValueError("Сумма пополнения счёта должна быть положительной")
        self._balance += amount
        self._add_operation("deposit", amount, "success")

    def withdraw(self, amount):  # Метод снятия со счёта
        if amount <= 0:
            raise ValueError("Сумма снятия со счёта должна быть положительной")
        if self._balance - amount < 0:
            self._add_operation("withdraw", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdraw", amount, "success")

    def get_balance(self):  # Геттер для баланса
        return self._balance

    def get_history(self):  # Вывод истории операций
        return pd.DataFrame(self.operation_history)

    def plot_history(
        self,
    ):  # Метод для формирования датафрейма из истории операций и его визуализация
        if not self.operation_history:
            print("Нет операций для отображения")
            return None
        history_df = pd.DataFrame(self.operation_history)
        x = history_df["date"]
        y = history_df["balance"]
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y %H:%M:%S"))
        plt.title(f"Изменение баланса счёта {self.account_number} с течением времени")
        plt.xlabel("Время")
        plt.ylabel("Баланс")
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.show()
        plt.close(fig)

    def analyze_large_transactions(self, n):  # Метод для вывода n крупных транзакций
        if not self.operation_history:
            print("Нет операций для анализа.")
            return None
        if n < 0:
            raise ValueError("Число операций может быть только положительным числом")
        transactions_df = pd.DataFrame(self.operation_history)
        success_operations_df = transactions_df[
            transactions_df["status"] == "success"
        ].copy()  # Явно копируем DataFrame, создавая независимую копию
        if success_operations_df.empty:
            print("Нет успешных операций для анализа.")
            return None
        success_operations_df.sort_values(
            by=["amount", "date"], ascending=[False, False], inplace=True
        )
        success_operations_df.reset_index(drop=True, inplace=True)
        return success_operations_df.head(n)


class CheckingAccount(Account):  # Класс-наследник базового класса - расчётный счёт
    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        self.account_type = "CheckingAccount"


class SavingsAccount(Account):  # Класс-наследник базового класса - сберегательный счёт
    def __init__(self, account_holder, balance):
        super().__init__(account_holder, balance)
        self.account_type = "SavingsAccount"

    def apply_interest(
        self, rate
    ):  # Выйчисляет выплату через год от начального остатка
        if rate < 0:
            raise ValueError("Процент не может быть отрицательным")
        return self._balance * (rate / 100)

    def withdraw(self, amount):  # Переопределенный метод снятия денег со счёта
        if amount <= 0:
            raise ValueError("Сумма снятия со счёта должна быть положительной")
        if (self._balance - amount < 0) or (self._balance / amount < 2):
            self._add_operation("withdraw", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdraw", amount, "success")


# ac1 = Account("Pf Kf", 200)
# ac2 = Account("Аsfsваы Аdfs", 4244)
"""
ac1.withdraw(300)
ac1.deposit(600)
ac1.withdraw(300)
ac2.withdraw(3000)
ac2.deposit(4060)
ac2.withdraw(77006)
ac2.withdraw(4456000)
ac2.deposit(4564060)
ac2.withdraw(3456006)
"""
ac2 = SavingsAccount("Аsfsваы Аdfs", 4244)
ac2.withdraw(3000)
ac2.deposit(4060)
ac2.withdraw(77006)
ac2.withdraw(4456000)
ac2.deposit(4564060)
ac2.withdraw(3456006)
print(ac2.get_history())
print(ac2.apply_interest(7))

print(ac2.analyze_large_transactions(2))
# print(ac1.plot_history())
print(ac2.plot_history())
