import time

from currency.models import ResponseLog


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        start = time.time()

        # Это выполнение вью-функции
        response = self.get_response(request)

        end = time.time()

        ResponseLog.objects.create(
            path=request.path,
            response_time=(end - start) * 1_000,
            status_code=response.status_code,
            request_method=request.method
        )

        return response
