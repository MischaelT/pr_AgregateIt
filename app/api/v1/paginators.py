from rest_framework.pagination import PageNumberPagination


class RatePagination(PageNumberPagination):

    """
        Pagination for rates page
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SourcePagination(PageNumberPagination):

    """
        Pagination for sources page
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class ContactUsPagination(PageNumberPagination):

    """
        Pagination for contact us lists page
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
