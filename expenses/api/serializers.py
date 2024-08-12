from django.db import transaction
from rest_framework import serializers
from expenses.models import Expense, ExpenseCategory

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer(many=True)

    class Meta:
        model = Expense
        fields = [
            "id", 
            "user", 
            "title", 
            "description", 
            "date", 
            "amount", 
            "category", 
            "frequency"
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        categories_data = validated_data.pop("category", [])
        user = self.context.get("request").user
        expense = None

        with transaction.atomic():
            expense = Expense.objects.create(user=user, **validated_data)

            categories_list = []
            for category_data in categories_data:
                category, created = ExpenseCategory.objects.get_or_create(user=user, name=category_data.get("name"))
                categories_list.append(category)
            
            expense.category.set(categories_list)
        return expense