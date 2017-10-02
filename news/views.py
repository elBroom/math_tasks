from django.shortcuts import render
from django.http import Http404

from .models import Article

# Create your views here.
def list(request):
    try:
        news = Article.objects.filter(is_public=True).all()
    except Article.DoesNotExist:
        news = []

    return render(request, 'news/list.html', {
            'title': 'News',
            'menu': 'news',
            'news': news,
        }
    )

def item(request, item_id):
    try:
        item = Article.objects.filter(pk=item_id).get()
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'news/item.html', {
            'title': item.title,
            'menu': 'news',
            'item': item,
        }
    )
