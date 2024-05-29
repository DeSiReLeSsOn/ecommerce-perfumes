import pytest 
from shop.tests.conftest import * 
from django.urls import reverse 
from reviews.forms import *

@pytest.mark.django_db
class TestViewsReviews:
    def test_gets_all_reviews(self, client, test_review):
        url = reverse('reviews:reviews')


        response = client.get(url) 


        assert response.status_code == 200 
        assert test_review in response.context['reviews'] 
        assert response.templates[0].name == 'reviews.html'
        assert 'review_form' in response.context
        assert 'comment_form' in response.context  



    def test_add_review(self, client, test_review):
        url = reverse('reviews:reviews')
        data = {
            'text': test_review.text
        }

        response = client.post(url, data=data)

        assert response.status_code == 200

        review = Review.objects.filter(pk=test_review.id)

        assert review.count() == 1




    def test_add_comment(self, client, test_review, test_comment_review):
        url = reverse('reviews:reviews')
        review_id = test_review.id
        data = {
            'text': test_comment_review.text
        }

        response = client.post(url, data=data, follow_redirects=True)

        assert response.status_code == 200

        review = Review.objects.get(pk=review_id)
        comments = review.comments.all()
        comment = comments.first()
        assert comments.count() == 1






    


