from django.shortcuts import render

# Create your views here.
def catalog(request):
    context= {
        'title': 'Home',
        'content': 'Главная страница'
    }
    return render(request, 'catalog/catalog.html', context)
def product(request):
    context= {
        'title': 'Home',
        'content': 'Главная страница'
    }
    return render(request, 'catalog/product.html', context)