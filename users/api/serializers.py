from common.constants import DEFAULT_EXPENSE_CATEGORIES
from expenses.models import ExpenseCategory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import (CharField, Serializer, ModelSerializer, ValidationError)
from django.contrib.auth import authenticate
from users.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['name'] = user.name

        return token
    
class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({'password': 'Passwords must match'})
        
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({'email': 'Email address must be unique'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        if user:
            for category in DEFAULT_EXPENSE_CATEGORIES:
                expense_categories = []
                expense_categories.append(ExpenseCategory(user=user, name=category))
                ExpenseCategory.objects.bulk_create(expense_categories)
        return user

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise ValidationError("Invalid credentials")
        return user