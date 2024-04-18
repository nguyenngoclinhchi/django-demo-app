from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_query_param = "page"
    page_size_query_param = 'page_size'  # Query parameter to set page size
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
