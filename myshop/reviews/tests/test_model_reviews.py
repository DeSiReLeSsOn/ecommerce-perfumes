import pytest 
from shop.tests.conftest import *   


@pytest.mark.django_db
class TestModelReviews:
    def test_model_reviews(self, client, test_review, test_user):
        review = test_review

        review_pk = review._get_pk_val()
        assert Review.objects.filter(pk=review_pk).count() == 1
        assert review.user == test_user 
        assert review.text == 'Test_review'


@pytest.mark.django_db
class TestModelCommentForReview:
    def test_comment(self, client, test_review, test_user, test_comment_review):
        test_comment = test_comment_review 

        test_comment_pk = test_comment._get_pk_val() 

        assert Comment.objects.filter(pk=test_comment_pk).count() == 1
        assert test_comment.review == test_review 
        assert test_comment.user == test_user 
        assert test_comment.text == 'Test_comment_review'
