import django_filters
from .models import Products


class ProductFilter(django_filters.FilterSet):


    CHOICES=(
        ('asc', 'Cena - od najniższej'),
        ('dsc', 'Cena - od najwyższej')
    )

    ordering = django_filters.ChoiceFilter(label='bla', choices=CHOICES, method='filter_b')
    class Meta:
        model = Products
        fields = {
            'title':['icontains']

        }

    def filter_b(self, queryset, name, value):
        expresion = 'price' if value == 'asc' else '-price'
        return queryset.order_by(expresion)