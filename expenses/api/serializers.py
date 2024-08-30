from django.db import transaction
from rest_framework import serializers
from expenses.models import Expense, ExpenseCategory

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer(many=True)
    amount = serializers.SerializerMethodField()
    parsed_amount = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = [
            "id", 
            "user", 
            "title", 
            "description", 
            "date", 
            "amount", 
            "parsed_amount",
            "category", 
            "frequency"
        ]
        read_only_fields = ["user"]

    def get_amount(self, instance):
        return float(instance.amount)
    
    def get_parsed_amount(self, instance):
        if (instance.user.currency == "INR"):
            return "₹" + str(instance.amount)
        elif (instance.user.currency == "USD"):
            return "$" + str(instance.amount)
        
        return instance.amount

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