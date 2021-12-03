from settings.settings import *  # noqa

DEBUG = False
# Когда селери находит эту настройку, то все таски будут выполняться как функции, игнорируя брокера. Не должно идти в прод
CELERY_TASK_ALWAYS_EAGER = True
