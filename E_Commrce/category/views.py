from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from category.models import Category
from category.serializers import CategorySerializer, CatSerializer, CategoryValidation
from E_Commrce.permission import StaffPermission, SuperUserPermission
from products.models import Products


class CategoryView(ModelViewSet):
    """
        Category will create here.
        Existing category should update ,destroy and retrieve by created user.
    """

    serializer_class = CategorySerializer
    permission_classes = [
        StaffPermission, SuperUserPermission
    ]
    # pagination_class = CustomPagination
    queryset = Category.objects.all()
    filterset_fields = ["categories", "tags__tag"]
    search_fields = ["categories", "tags__tag"]
    ordering_fields = ['id', "tag"]

    # renderer_classes = [CustomRenderer,]

    def get_serializer_class(self) -> Any:
        if self.request.version == 'v1':
            return self.serializer_class
        return CatSerializer

    def list(self, request, *args, **kwargs) -> Response:
        page_size = self.request.query_params.get('page_size')
        if page_size and page_size.lower() == 'all':
            self.pagination_class.page_size = len(self.queryset)
        response = super().list(self, request)

        return Response({'message': "successfully", 'result': response.data})

    # @action(detail=False, methods=['post'])
    # def all_queryset(self, request):
    #     items = self.query_set
    #     serializer = self.serializer_class(items, many=True)
    #     return Response({"message": "successfully added.", "items": serializer.data})

    @action(detail=False, methods=["post"])
    def category_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def category_product(self, request, pk):
        response = Products.objects.filter(category__id=pk)
        return Response(response)


class CategoryValidationView(CreateAPIView):
    serializer_class = CategoryValidation
    queryset = Category.objects.all()
