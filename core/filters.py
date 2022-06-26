from datetime import datetime

import django_filters
from django.db.models import F, Q

from core.models import Shop

STATUS_CHOICES = (
    (0, 'Closed'),
    (1, 'Open')
)


class ShopFilter(django_filters.FilterSet):
    open = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method='shop_opening_filter'
    )

    class Meta:
        model = Shop
        fields = ['open', 'city', 'street']

    def shop_opening_filter(self, queryset, name, value):
        current_time = datetime.now().strftime("%H:%M:%S")

        # магазины закрывающиеся в день открытия
        schedule_queryset = queryset.filter(open_time__lte=F('closing_time'))

        # магазины закрывающиеся на следующий день после открытия
        scheduler_queryset_reversed = queryset.filter(open_time__gte=F('closing_time'))

        if value == '1':
            always_open_shops = queryset.filter(open_time=F('closing_time'))
            schedule_queryset = schedule_queryset.filter(
                open_time__lte=current_time,
                closing_time__gte=current_time
            )
            scheduler_queryset_reversed = scheduler_queryset_reversed.filter(
                Q(open_time__lte=current_time) | Q(closing_time__gte=current_time))
            resulting_queryset = schedule_queryset | scheduler_queryset_reversed | always_open_shops
        else:
            schedule_queryset = schedule_queryset.filter(
                Q(open_time__gte=current_time) | Q(closing_time__lte=current_time)).exclude(open_time=F('closing_time'))
            scheduler_queryset_reversed = scheduler_queryset_reversed.filter(
                open_time__gte=current_time, closing_time__lte=current_time)
            resulting_queryset = schedule_queryset | scheduler_queryset_reversed

        return resulting_queryset
