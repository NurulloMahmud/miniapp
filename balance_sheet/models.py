from django.db import models


class IncomeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Income Category"
        verbose_name_plural = "Income Categories"
        db_table = "income_categories"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"
        db_table = "expense_categories"


class Income(models.Model):
    from users.models import TelegramUser

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
        db_table = "incomes"


class Expense(models.Model):
    from users.models import TelegramUser

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        db_table = "expenses"

