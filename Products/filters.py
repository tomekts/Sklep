import django_filters
from .models import Products


class ProductFilter(django_filters.FilterSet):


    CHOICES=(
        ('ros', 'Rosnoco cena'),
        ('mal', 'Malejąco cena')
    )

    ordering = django_filters.ChoiceFilter(label='bla', choices=CHOICES, method='filter_b')
    class Meta:
        model = Products
        fields = {
            'title':['icontains']

        }

    def filter_b(self, queryset, name, value):
        expresion = 'price' if value == 'ros' else '-price'
        return queryset.order_by(expresion)