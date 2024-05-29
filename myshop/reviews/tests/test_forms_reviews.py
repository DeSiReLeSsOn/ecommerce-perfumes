import pytest 
from shop.tests.conftest import * 
from reviews.forms import ReviewCreateForm, CommentForm


@pytest.mark.django_db
class TestReviewForms:
    def test_review_form(self, client, test_review):
        data = {'text': test_review.text} 

        form = ReviewCreateForm(data=data) 


        assert form.is_valid() == True 
        assert form.cleaned_data['text'] == 'Test_review'  



@pytest.mark.django_db
class TestCommentReviewForms:
    def test_comment(self, test_comment_review):
        data = {'text': test_comment_review.text} 


        form = CommentForm(data=data) 

        assert form.is_valid() == True
        assert form.cleaned_data['text'] == 'Test_comment_review'



