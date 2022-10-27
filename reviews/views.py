from django.shortcuts import render
from .models import Review, Comment
from reviews.models import Review
from django.db.models import Count

# Create your views here.

# 글 목록
def index(request):
    reviews = Review.objects.annotate(Count('commnet')).order_by('-pk')
    context = {
        'reviews' : reviews
    }
    return render(request, 'reviews/index.html', context)