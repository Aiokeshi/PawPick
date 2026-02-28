from django.shortcuts import render
from catalog.models import Cards
# Create your views here.
def catalog(request):
    catalog = Cards.objects.all()
    context= {
        'title': 'Home',
        "catalog": catalog
    }
    return render(request, 'catalog/catalog.html', context)
def product(request):
    context= {
        'title': 'Home',
        'content': 'Главная страница'
    }
    return render(request, 'catalog/card.html', context)