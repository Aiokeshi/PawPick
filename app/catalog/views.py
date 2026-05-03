from django.shortcuts import render
from catalog.models import Cards, TagCategory


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
    # Получаем карточку или возвращаем 404
    card = Cards.objects.get(slug=card_slug)
    
    # Получаем выбранные теги из GET-параметров (если переход был из каталога)
    selected_tags = request.GET.getlist('tags')
    selected_tags_ids = [int(i) for i in selected_tags if i.isdigit()]
    
    # Получаем все теги этой карточки
    card_tags = card.tags.all()
    
    # Получаем все категории тегов для фильтрации (если нужно показать все возможные теги)
    categories = TagCategory.objects.prefetch_related('tags')
    
    context = {
        'card': card,
        'selected_tags': selected_tags_ids,  # ID выбранных тегов
        'card_tags': card_tags,              # Теги, привязанные к карточке
        'categories': categories,             # Все категории с тегами
    }
    
    return render(request, 'catalog/card.html', context=context)