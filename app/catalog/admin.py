from django.contrib import admin

from catalog.models import Cards, FavoriteCard, Tag, TagCategory


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    filter_vertical = ('tags',)
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(FavoriteCard)
class FavoriteCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'card__name')
