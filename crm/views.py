from rest_framework import viewsets, status
from rest_framework.response import Response

from crm.models import Product, Sale, Company
from crm.serializer import ProductSerializer, SaleSerializer, CompanySerializer, CompanyFinancialSerializer, UserSerializer

#filters
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#authentication and authorization
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'name']
    search_fields = ['name']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'product']
    search_fields = ['product', 'sale_date']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super(SaleViewSet, self).create(request, *args, **kwargs)
        
        sale = Sale.objects.get(id=response.data['id'])
        product = sale.product

        if sale.quantity_sold <= product.quantity:
            product.quantity -= sale.quantity_sold
            company = Company.objects.get(id=1)
            company.total_revenue += sale.quantity_sold * sale.product.price
            
            product.save()
            company.save()
            
            return response
        raise ValueError('Quantity above limit')
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            product = instance.product
            quantity_sold = instance.quantity_sold
            company = Company.objects.get(id=1)
            
            product.quantity += quantity_sold
            company.total_revenue -= quantity_sold * instance.product.price
            
            product.save()
            company.save()
            
            return super().delete(request, *args, **kwargs)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'company_name']
    search_fields = ['company_name']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

class CompanyFinancialViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanyFinancialSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.is_authenticated:
            self.permission_denied(
                request, message="Você precisa estar autenticado como admin para acessar esta view."
            )
        elif request.user.username != 'admin':
            self.permission_denied(
                request, message="Você não tem permissão para acessar esta view."
            )

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]