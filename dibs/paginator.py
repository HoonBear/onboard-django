from rest_framework.pagination import CursorPagination


class DibsGroupPaginator(CursorPagination):
    page_size = 3
    cursor_query_param = 'cursor'
    ordering = '-createdAt'