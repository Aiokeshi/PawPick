from django.contrib import admin
from catalog.models import Cards, Tag, TagCategory

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    filter_vertical = ('tags',)
# Register your models here.
@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

