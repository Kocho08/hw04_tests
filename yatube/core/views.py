from django.shortcuts import render


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


def bad_request(request, exception):
    return render(request, 'core/400.html', {'path': request.path}, status=400)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')
