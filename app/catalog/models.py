from django.db import models

# Create your models here.
class Cards(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URl')
    description=models.TextField(blank=True, null=True, verbose_name='Описание')
    image=models.ImageField(upload_to='card_images', blank=True,null=True,verbose_name='Изображение')
    tages=models.TextField(blank=True, null=True, verbose_name='теги')

    class Meta:
        db_table='card'
        verbose_name='Карточки'
        verbose_name_plural='Карта'
