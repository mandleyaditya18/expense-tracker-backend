from django.db import models
from users.models import User
from datetime import date
from common.constants import EXPENSE_FREQUENCY_CHOICES

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ExpenseCategory(BaseModel):
    user = models.ForeignKey(User, related_name="expense_categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_name = "expense_category"
        verbose_name = "expense_category"
        verbose_name_plural = "expense_categories"


class Expense(BaseModel):
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    date = models.DateField(default=date.today, blank=False, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ManyToManyField(ExpenseCategory, related_name="expenses")
    frequency = models.CharField(max_length=255, choices=EXPENSE_FREQUENCY_CHOICES, default="one_time")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "expense"
        verbose_name = "expense"
        verbose_name_plural = "expenses"
