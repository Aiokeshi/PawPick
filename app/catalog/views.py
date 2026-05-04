from django.shortcuts import get_object_or_404, render

from catalog.models import Cards, Tag, TagCategory


HIDDEN_TAG_CATEGORY = 'Скрытые теги'


def _get_visible_tag_ids():
    return set(
        Tag.objects
        .exclude(category__name=HIDDEN_TAG_CATEGORY)
        .values_list('id', flat=True)
    )


def _clean_selected_tags(selected_tags):
    visible_tag_ids = _get_visible_tag_ids()

    return [
        int(tag_id)
        for tag_id in selected_tags
        if tag_id.isdigit() and int(tag_id) in visible_tag_ids
    ]


def catalog(request):
    cards = Cards.objects.all()

    selected_tags = request.GET.getlist('tags')
    selected_tags_ids = _clean_selected_tags(selected_tags)

    for tag_id in selected_tags_ids:
        cards = cards.filter(tags__id=tag_id)

    categories = (
        TagCategory.objects
        .exclude(name=HIDDEN_TAG_CATEGORY)
        .prefetch_related('tags')
    )

    return render(request, 'catalog/catalog.html', {
        'catalog': cards.distinct(),
        'categories': categories,
        'selected_tags': selected_tags_ids,
        'selected_tags_query': request.GET.urlencode(),
    })


def card(request, card_slug):
    card = get_object_or_404(Cards, slug=card_slug)

    selected_tags = request.GET.getlist('tags')
    selected_tags_ids = _clean_selected_tags(selected_tags)

    card_tags = card.tags.exclude(category__name=HIDDEN_TAG_CATEGORY)

    selected_tag_names = list(
        Tag.objects
        .filter(id__in=selected_tags_ids)
        .exclude(category__name=HIDDEN_TAG_CATEGORY)
        .values_list('name', flat=True)
    )

    categories = (
        TagCategory.objects
        .exclude(name=HIDDEN_TAG_CATEGORY)
        .prefetch_related('tags')
    )

    context = {
        'card': card,
        'selected_tags': selected_tags_ids,
        'selected_tag_names': selected_tag_names,
        'card_tags': card_tags,
        'categories': categories,
    }

    return render(request, 'catalog/card.html', context=context)
