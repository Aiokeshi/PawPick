from django.shortcuts import render
from catalog.models import Cards, TagCategory
# Create your views here.
# def catalog(request):
#     catalog = Cards.objects.all()
#     context= {
#         'title': 'Home',
#         "catalog": catalog
#     }
#     return render(request, 'catalog/catalog.html', context)

def catalog(request):
    cards = Cards.objects.all()

    selected_tags = request.GET.getlist('tags')

    for tag_id in selected_tags:
        cards = cards.filter(tags__id=tag_id)

    categories = TagCategory.objects.prefetch_related('tags')

    return render(request, 'catalog/catalog.html', {
        'catalog': cards.distinct(),
        'categories': categories,
        'selected_tags': [int(i) for i in selected_tags],
    })


def card(request, card_slug):
    card = Cards.objects.get(slug=card_slug)
    context= {
        'card': card
    }
    return render(request, 'catalog/card.html', context=context)