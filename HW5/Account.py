from datetime import datetime
import pandas as pd
from matplotlib import dates as mdates, pyplot as plt
import re
import os


class Account:  # Базовый класс - банковский счёт
    _account_counter = 100000

    def __init__(self, account_holder, balance=0):
        self.account_type = "BaseAccount"
        self.valid_operations = ("deposit", "withdraw")
        self.valid_status = ("success", "fail")
        self._validate_balance(balance)
        self._validate_holder(account_holder)
        self._balance = balance
        self.holder = account_holder
        Account._account_counter += 1
        self.account_number = f"ACC-{self._account_counter}"
        self.operation_history = []

    def _validate_holder(self, account_holder): # Валидация имени владельца счёта
        if not re.fullmatch(r"^[A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+", account_holder):
            raise ValueError("Неверный формат имени владельца счёта")

    def _validate_balance(self, balance): # Валидация баланса
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")

    def _validate_amount(self, amount): # Валидация суммы
        if amount < 0:
            raise ValueError("Сумма должна быть положительной")

    def _operations_history_empty(self):# Проверка на пустоту списка операций
        if not self.operation_history:
            print("Отсутствуют операции по данному счёту")
            return True

    def _add_operation( 
        self, operation_type, amount, status):# Метод для добавления операций в историю
        operation = {
            "operation_type": operation_type,
            "account_type": self.account_type,
            "amount": amount,
            "date": datetime.now(),
            "balance_after": self._balance,
            "status": status,
        }
        self.operation_history.append(operation)

    def deposit(self, amount):  # Метод пополнения счёта
        self._validate_amount(amount)
        self._balance += amount
        self._add_operation("deposit", amount, "success")

    def withdraw(self, amount):  # Метод снятия со счёта
        self._validate_amount(amount)
        if self._balance - amount < 0:
            self._add_operation("withdraw", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdraw", amount, "success")

    def get_balance(self):  # Геттер для баланса
        return self._balance

    def get_history(self):  # Вывод истории операций
        if self._operations_history_empty():
            return None
        return pd.DataFrame(self.operation_history)

    def plot_history(
        self,
    ):  # Метод для формирования датафрейма из истории операций и его визуализация
        if self._operations_history_empty():
            return None
        history_df = pd.DataFrame(self.operation_history)
        x = history_df["date"]
        y = history_df["balance_after"]
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
        return fig

    def analyze_large_transactions(self, n):  # Метод для вывода n крупных транзакций
        if self._operations_history_empty():
            return None
        if n < 0:
            raise ValueError("Число операций может быть только положительным числом")
        transactions_df = pd.DataFrame(self.operation_history)
        success_transactions_df = transactions_df[
            transactions_df["status"] == "success"
        ].copy()  # Явно копируем DataFrame, создавая независимую копию
        if success_transactions_df.empty:
            print("Нет успешных транзакций")
            return None
        success_transactions_df.sort_values(
            by=["amount", "date"], ascending=[False, False], inplace=True
        )
        success_transactions_df.reset_index(drop=True, inplace=True)
        return success_transactions_df.head(n)

    def load_dirty_file(self, path):  # Метод для загрузки файла и обновления баланса
        _, extansion = os.path.splitext(path)
        if extansion == ".csv":
            dirty_df = pd.read_csv(path)
        elif extansion == ".json":
            dirty_df = pd.read_json(path)
        else:
            print(f"Файл с расширением {extansion} не поддерживатеся")
            return None
        self.operation_history = (
            self.filter_history(dirty_df).sort_values(by="date").to_dict("records")
        )
        self._balance = self.operation_history[-1]["balance_after"]

    def filter_history(
        self, dirty_df
    ):  # Метод фильтрации истории операций из внешнего файла
        cleaned_df = dirty_df[
            (dirty_df["account_number"] == self.account_number)
            & (dirty_df["account_type"] == self.account_type)
            & (pd.to_datetime(dirty_df["date"], errors="coerce").notna())
            & (dirty_df["operation"].isin(self.valid_operations))
            & (dirty_df["amount"] > 0)
            & (dirty_df["balance_after"] >= 0)
            & (dirty_df["status"].isin(self.valid_status))
        ].copy()
        cleaned_df = cleaned_df.dropna()
        if cleaned_df.empty:
            print(f"Нет операций по счёту {self.account_number}")
        return cleaned_df


class CheckingAccount(Account):  # Класс-наследник базового класса - расчётный счёт
    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        self.account_type = "checking"


class SavingsAccount(Account):  # Класс-наследник базового класса - сберегательный счёт
    def __init__(self, account_holder, balance):
        super().__init__(account_holder, balance)
        self.account_type = "savings"
        self.valid_operations = ("deposit", "withdraw", "interest")

    def apply_interest(
        self, rate
    ):  # Выйчисляет выплату через год от начального остатка, только расчитывает
        if rate < 0:
            raise ValueError("Процент не может быть отрицательным")
        return self._balance * (rate / 100)

    def withdraw(self, amount):  # Переопределенный метод снятия денег со счёта
        self._validate_amount(amount)
        if (self._balance - amount < 0) or (self._balance / amount < 2):
            self._add_operation("withdraw", amount, "fail")
        else:
            self._balance -= amount
            self._add_operation("withdraw", amount, "success")


# Тестирование

# 1. Создание аккаунта с неправильным именем
try:
    bad_acc1 = Account("ivan ivanov")  # Имя без заглавных букв
except ValueError as e:
    print("1.", e)

# 2. Создание аккаунта с отрицательным балансом
try:
    bad_acc2 = Account("Иван Иванов", -100)
except ValueError as e:
    print("2.", e)

# 3. Попытка пополнить отрицательной суммой
acc = Account("Иван Иванов", 100)
try:
    acc.deposit(-50)
except ValueError as e:
    print("3.", e)

# 4. Попытка снять больше, чем есть на счете
acc.withdraw(200)  # Баланс 100, снимаем 200
print(
    "4.", acc.get_balance()
)  # Баланс должен остаться 100, операция зафиксирована как fail

# 5. Попытка загрузить файл с неправильным расширением
print("5.")
acc.load_dirty_file(
    "data.txt"
)  # Должно вывести сообщение о неподдерживаемом расширении


# 6. Попытка снять больше 50% для SavingsAccount
savings_acc = SavingsAccount("Петр Петров", 1000)
try:
    savings_acc.withdraw(600)  # 60% от 1000, должно быть запрещено
except Exception as e:
    print("6.", e)
print("6.", savings_acc.get_balance())  # Баланс должен остаться 1000

# 7. Попытка применить отрицательный процент
try:
    savings_acc.apply_interest(-5)
except ValueError as e:
    print("7.", e)

# Создаем аккаунт
acc = Account("Иван Иванов", 1000)

# Проверка пополнения
acc.deposit(500)
print(acc.get_balance())  # Ожидается 1500

# Проверка снятия
acc.withdraw(300)
print(acc.get_balance())  # Ожидается 1200

# Попытка снять больше, чем есть
acc.withdraw(2000)
print(acc.get_balance())  # Ожидается 1200, операция должна быть зафиксирована как fail

# Проверка истории
history = acc.get_history()
print(history)

# Визуализация
acc.plot_history()
