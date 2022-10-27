from django.shortcuts import redirect, render

from reviews.forms import ReviewForm
from .models import Review, Comment
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.

# 글 목록
def index(request):
    reviews = Review.objects.annotate(Count('commnet')).order_by('-pk')
    context = {
        'reviews' : reviews
    }
    return render(request, 'reviews/index.html', context)

# 글 조회
def detail(request, pk):
    reviews = Review.objects.select_related('user').order_by('-pk')
    context = {
        'reviews' : reviews,
    }
    return render(request, 'reviews/detail.html', context)

# 글 작성
@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form'  : review_form
    }
    return render(request, 'reviews/form.html', context)