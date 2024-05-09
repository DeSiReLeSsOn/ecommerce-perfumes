from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewCreateForm, CommentForm



# def show_reviews(request):
#     reviews = Review.objects.all().order_by('-created')

#     if request.method == 'POST':
#         form = ReviewCreateForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.save()
#             return redirect('reviews:reviews')
#     else:
#         form = ReviewCreateForm()

#     return render(request, 'reviews.html', {'reviews': reviews, 'form': form})


def show_reviews(request, review_id=None):
    reviews = Review.objects.all().order_by('-created')

    if request.method == 'POST':
        if 'review_text' in request.POST:
            form = ReviewCreateForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('reviews:reviews')
        elif 'comment_text' in request.POST:
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.review = review
                comment.save()
                return redirect('reviews:reviews')
    else:
        review_form = ReviewCreateForm()
        comment_form = CommentForm()

    return render(request, 'reviews.html', {'reviews': reviews, 'review_form': review_form, 'comment_form': comment_form})
