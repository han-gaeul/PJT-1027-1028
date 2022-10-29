from django.shortcuts import redirect, render

from reviews.forms import CommentForm, ReviewForm
from .models import Review, Comment
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.

# 글 목록
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews' : reviews
    }
    return render(request, 'reviews/index.html', context)

# 글 조회
def detail(request, pk):
    reviews = Review.objects.get(pk=pk)
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

# 글 수정
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('reviews:detail', review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        'review_form' : review_form
    }
    return render(request, 'reviews/form.html', context)

# 글 삭제
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:index')
    context = {
        'review' : review
    }
    return render(request, 'reviews/index.html', context)

# 댓글 작성
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect('reviews:detail', pk)

# 댓글 삭제
def comment_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('reviews:detail', pk)

# 좋아요
@login_required
def like(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('reviews;detail', pk)