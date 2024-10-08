from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import ExpenseSerializer, ExpenseCategorySerializer
from expenses.models import Expense

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.expenses.filter(is_deleted=False).order_by("-created_at")

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        expense = get_object_or_404(Expense, id=kwargs['pk'], user=request.user)
        expense.is_deleted = True
        expense.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        user = request.user
        categories = user.expense_categories.all()
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response(serializer.data)
