from datetime import datetime
import pandas as pd
from matplotlib import dates as mdates, pyplot as plt
import re
import os

class Account:  # Базовый класс - банковский счёт
    _account_counter = 100000

    def __init__(self, account_holder, balance=0):
        self.account_type = "BaseAccount"
        self.valid_operations = ("deposit","withdraw")
        self.valid_status = ("success","fail")
        self._validate_balance(balance)
        self._validate_holder(account_holder)
        self._balance = balance
        Account._account_counter += 1
        self.holder = account_holder
        self.account_number = f"ACC-{self._account_counter}"
        self.operation_history = []

    def _validate_holder(self, account_holder):
        if not re.fullmatch(r"^[A-ZА-Я][a-zа-я]+ [A-ZА-Я][a-zа-я]+", account_holder):
            raise ValueError("Неверный формат имени владельца счёта") 
        
    def _validate_balance(self, balance):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
    
    def _validate_amount(self, amount):
        if amount < 0:
            raise ValueError("Сумма должна быть положительной")
    
    def _operations_history_empty(self):
        if not self.operation_history:
            print("Отсутствуют операции по данному счёту")
            return True

    def _add_operation(
        self, operation_type, amount, status
    ):  # Метод для добавления операций в историю
        operation = {
            "operation_type": operation_type,
            "account_type": self.account_type,
            "amount": amount,
            "date": datetime.now(),
            "balance": self._balance,
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

    def plot_history(self):  # Метод для формирования датафрейма из истории операций и его визуализация
        if self._operations_history_empty():
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

    def load_dirty_file(self,path):
        _, extansion = os.path.splitext(path)
        if extansion == ".csv":
            dirty_df = pd.read_csv(path)
        elif extansion == ".json":
            dirty_df = pd.read_json(path)
        else:
            print(f"Файл с расширением {extansion} не поддерживатеся")
            return None
        print(self.clean_history(dirty_df))
        
    def clean_history(self, df):  # Метод очистки истории для CheckingAccount (доступны только deposit и withdraw)
        print(self.valid_operations, '               ', self.account_type, '    ', self.account_number)
        print(self.account_type)
        print(df.iloc[35,1] == self.account_type)
        cleaned_df = df[
            (df['account_number'] == self.account_number) &
            (df['account_type'] == self.account_type) &
            (pd.to_datetime(df['date'], errors='coerce').notna()) &
            (df['operation'].isin(self.valid_operations)) &
            (df['amount'] > 0) &
            (df['balance_after'] >= 0) &
            (df['status'].isin(self.valid_status))
            #Баланс после операции не может быть отрицательным 
        ].copy()
        # Удаление строк с NaN в operation (опечатки)
        cleaned_df = cleaned_df.dropna()
        
        return cleaned_df


class CheckingAccount(Account):  # Класс-наследник базового класса - расчётный счёт
    def __init__(self, account_holder, balance=0):
        super().__init__(account_holder, balance)
        self.account_type = "checking"

class SavingsAccount(Account):  # Класс-наследник базового класса - сберегательный счёт
    def __init__(self, account_holder, balance):
        super().__init__(account_holder, balance)
        self.account_type = "savings"
        self.valid_operations = ("deposit","withdraw","interest")
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


#ac1 = Account("Pf Kf", 200)
#ac2 = Account("Аsfsваы Аdfs", 4244)
'''
ac1.withdraw(300)
ac1.deposit(600)
ac1.withdraw(300)
ac1.withdraw(3000)
ac1.deposit(4060)
ac1.withdraw(77006)
ac1.withdraw(4456000)
ac1.deposit(4564060)
ac1.withdraw(3456006)

print(ac1.get_history())
print(ac1.analyze_large_transactions(2))
#print(ac1.plot_history())
print(ac1.plot_history())
'''
ac2 = SavingsAccount("Аsfsваы Аdfs", 4244)
ac2.load_dirty_file(r"HW5\transactions_dirty.csv")
'''
ac2.withdraw(3000)
ac2.deposit(4060)
ac2.withdraw(77006)
ac2.withdraw(4456000)
ac2.deposit(4564060)
ac2.withdraw(3456006)

print(ac2.get_history())
print(ac2.apply_interest(7))
print(ac2.analyze_large_transactions(2))
#print(ac1.plot_history())
print(ac2.plot_history())
'''