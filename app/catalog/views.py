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


def card(request, card_slug):
    card = Cards.objects.get(slug=card_slug)
    context= {
        'card': card
    }
    return render(request, 'catalog/card.html', context=context)