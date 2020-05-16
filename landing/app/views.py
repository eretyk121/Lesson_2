from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    page_from = request.GET.get('from-landing')
    if page_from == 'test':
        msg = render_to_response('landing_alternate.html')
        counter_click['test'] += 1
    elif page_from == 'original':
        msg = render_to_response('landing.html')
        counter_click['original'] += 1
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render_to_response('index.html')


def landing(request):
    variant = request.GET.get('ab-test-arg')
    if variant == 'test':
        msg = render_to_response('landing_alternate.html')
        counter_show['test'] += 1
    else:
        msg = render_to_response('landing.html')
        counter_show['main'] += 1
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    # return render_to_response('landing.html')
    return msg

def stats(request):
    try:
        from_original = counter_click['original'] / counter_show['main']
    except ZeroDivisionError:
        from_original = 'Переходы со страницы original отсутствуют'
    try:
        from_test = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        from_test = 'Переходы со страницы test отсутствуют'
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    return render_to_response('stats.html', context={
        'test_conversion': from_test,
        'original_conversion': from_original,
    })
