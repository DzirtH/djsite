from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить издание", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},

        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        years = Category.objects.all()
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = menu
        context['years'] = years
        if 'year_selected' not in context:
            context['year_selected'] = 0
        return context
