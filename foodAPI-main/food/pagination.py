from rest_framework import pagination
from rest_framework.response import Response

class MyPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'current': self.request.build_absolute_uri(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data
        })

    def get_first_link(self):
        return self.request.build_absolute_uri(self.page.number - self.page.number + 1) if self.page.number > 1 else None

    def get_last_link(self):
        last_page = self.page.paginator.num_pages
        return self.request.build_absolute_uri(self.page.number - self.page.number + last_page) if self.page.number < last_page else None
