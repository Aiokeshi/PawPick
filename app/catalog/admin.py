from django.contrib import admin

from catalog.models import Cards, FavoriteCard, Tag, TagCategory


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    filter_vertical = ('tags',)
    list_display = ('name', 'owner')
    readonly_fields = ('owner',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user

        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is None:
            return True

        return obj.owner == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj is None:
            return True

        return obj.owner == request.user


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
