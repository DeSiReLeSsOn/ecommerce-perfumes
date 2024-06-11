from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

# Основные настройки Gunicorn
bind = '0.0.0.0:' + environ.get('PORT', '8000')  # Слушает на всех доступных интерфейсах (включая localhost)
workers = max_workers()  # Использует количество доступных процессоров
worker_class = 'gevent'  # Использование gevent для асинхронных операций
max_requests = 1000  # Максимальное количество запросов для рабочего процесса
reload = True  # Перезагрузка Gunicorn при изменении кода

# Дополнительные настройки (опционально)
accesslog = '-'  # Вывод логов доступа в стандартный поток вывода
errorlog = '-'  # Вывод ошибок в стандартный поток вывода
timeout = 120  # Тайм-аут для запросов (в секундах)

# Окружение Django
env = {
    'DJANGO_SETTINGS_MODULE': 'myshop.settings.prod'
}

# Имя приложения
name = 'myshop'