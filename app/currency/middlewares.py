<<<<<<< HEAD
import time

from currency.models import ResponseLog

=======
from currency.models import ResponseLog
import time
>>>>>>> develop

class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        start = time.time()

        # Это выполнение вью-функции
        response = self.get_response(request)

        end = time.time()

<<<<<<< HEAD
        ResponseLog.objects.create(
            path=request.path,
            response_time=(end - start) * 1_000,
            status_code=response.status_code,
        )

        return response
=======
        print(f'Time: {end - start}')

        ResponseLog.objects.create(
            path = request.path,
            response_time = (end - start)* 1_000,
            status_code = response.status_code,
        )

        return response
>>>>>>> develop
