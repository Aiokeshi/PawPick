from django.db import models

# Create your models here.
class Cards(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URl')
    height=models.TextField(blank=True, null=True, verbose_name='Рост')
    weight=models.TextField(blank=True, null=True, verbose_name='Вес')
    age=models.TextField(blank=True, null=True, verbose_name='Продолжительность жизни')
    furr=models.TextField(blank=True, null=True, verbose_name='Тип шерсти')
    furrColors=models.TextField(blank=True, null=True, verbose_name='Окрасы')
    imageMain=models.ImageField(upload_to='card_images', blank=True,null=True,verbose_name='Главное изображение')
    imageScnd=models.ImageField(upload_to='card_images', blank=True,null=True,verbose_name='Изображение')
    imageThrd=models.ImageField(upload_to='card_images', blank=True,null=True,verbose_name='Изображение')
    tages=models.TextField(blank=True, null=True, verbose_name='Теги')
    description=models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table='card'
        verbose_name='Карточки'
        verbose_name_plural='Карта'
