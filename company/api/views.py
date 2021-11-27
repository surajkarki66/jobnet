from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from company.api.filters import CompanyFilter
from company.api.serializers import CompanySerializer, CompanyTypeSerializer, EmployeeTypeSerializer, EmployeeSerializer
from company.models import Company, CompanyType, EmployeeType, Employee

from lib.api.permissions import IsObjectEmployerOrReadOnly, IsEmployer, IsEmployerOwnedEmployeeOrReadOnly


class CompanyModelViewSetAPI(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsObjectEmployerOrReadOnly,)
    filterset_class = CompanyFilter
    search_fields = ('persian_name', 'english_name')

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)


class CompanyTypeModelViewSetAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                 mixins.ListModelMixin, GenericViewSet):
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = (IsEmployer,)
    search_fields = ('type',)


class EmployeeTypeModelViewSetAPI(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin, GenericViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    permission_classes = (IsEmployer,)
    search_fields = ('type',)


class EmployeeModelViewSetAPI(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsEmployerOwnedEmployeeOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.employer.company)
