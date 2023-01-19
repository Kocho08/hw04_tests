from django.utils import timezone


def year(request):
    """Добавляет переменную с текущим годом."""
    current_datetime = timezone.now()
    return {
        'year': current_datetime.year
    }
