from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.expenses.all().order_by("-created_at")
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)