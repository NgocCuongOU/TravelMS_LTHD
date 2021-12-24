from rest_framework.pagination import PageNumberPagination


class BasePostPagination(PageNumberPagination):
    page_size = 3


class BaseTourPagination(PageNumberPagination):
    page_size = 6