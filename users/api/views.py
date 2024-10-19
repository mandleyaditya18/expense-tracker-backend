from datetime import datetime
from django.db.models import Sum
from expenses.models import Expense
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, MyTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token_serializer = MyTokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)
            access_token = refresh.access_token
            return Response({
                "refresh": str(refresh),
                "access": str(access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # Use the custom serializer for token
            token_serializer = MyTokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def total_expense_by_month(self, request):
        month = request.query_params.get("month")

        if not month:
            return Response(
                {"error": "Month params is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(month, "%m-%y")
            print({date})
            total_expense = Expense.objects.filter(
                user=request.user,
                date__year=date.year,
                date__month=date.month,
                is_deleted=False
            ).aggregate(total=Sum("amount"))["total"] or 0

            return Response({
                "month": month,
                "total_expense": total_expense
            })
        except:
            return Response(
                {"error": "Invalid month format. Use MM-YY."},
                status=status.HTTP_400_BAD_REQUEST
            )

