from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from category.models import Category
from category.serializers import CategorySerializer, CatSerializer
from E_Commrce.pagination import CustomPagination
from E_Commrce.permission import StaffPermission


class CategoryView(ModelViewSet):
    """
        Category will create here.
        Existing category should update ,destroy and retrieve by created user.
    """

    serializer_class = CategorySerializer
    permission_classes = [
        StaffPermission

    ]
    # pagination_class = CustomPagination
    queryset = Category.objects.all()
    filterset_fields = ["categories", "tags__tag"]
    search_fields = ["categories", "tags__tag"]
    ordering_fields = ['id', "categories", "tag"]

    def get_serializer_class(self) -> Any:
        if self.request.version == 'v1':
            return self.serializer_class
        return CatSerializer

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page_size = self.request.query_params.get('page_size')

        if page_size:
            self.pagination_class.page_size = page_size
            if page_size.lower() == 'all':
                self.pagination_class.page_size = len(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'message': "successfully", 'result': serializer.data})

    # @action(detail=False, methods=['post'])
    # def all_queryset(self, request):
    #     items = self.query_set
    #     serializer = self.serializer_class(items, many=True)
    #     return Response({"message": "successfully added.", "items": serializer.data})

    @action(detail=False,methods=["post"])
    def category_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

