from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from catalog.models import Cards, FavoriteCard, Tag, TagCategory


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


def _get_favorite_card_ids(request):
    if not request.user.is_authenticated:
        return set()

    return set(
        FavoriteCard.objects
        .filter(user=request.user)
        .values_list('card_id', flat=True)
    )


def _safe_next_url(request):
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')

    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        return next_url

    return reverse('catalog:catalog')


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
        'favorite_card_ids': _get_favorite_card_ids(request),
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

    return render(request, 'catalog/card.html', {
        'card': card,
        'selected_tags': selected_tags_ids,
        'selected_tag_names': selected_tag_names,
        'card_tags': card_tags,
        'categories': categories,
        'favorite_card_ids': _get_favorite_card_ids(request),
    })


@login_required(login_url='register:login')
def favorites(request):
    cards = (
        Cards.objects
        .filter(favorite_users__user=request.user)
        .order_by('-favorite_users__created_at')
        .distinct()
    )

    return render(request, 'catalog/favorites.html', {
        'favorites': cards,
        'favorite_card_ids': _get_favorite_card_ids(request),
    })


@require_POST
@login_required(login_url='register:login')
def toggle_favorite(request, card_slug):
    card = get_object_or_404(Cards, slug=card_slug)

    favorite, created = FavoriteCard.objects.get_or_create(
        user=request.user,
        card=card
    )

    if not created:
        favorite.delete()

    return redirect(_safe_next_url(request))
