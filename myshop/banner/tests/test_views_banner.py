import pytest 
from shop.tests.conftest import *
from django.urls import reverse 


@pytest.mark.django_db
class TestViewsBanner:
    def test_gets_all_banners(self, client, test_banner):
        url = reverse('banner:banner')

        response = client.get(url)


        assert response.status_code == 200 
        assert response.templates[0].name == 'banner.html'
        assert list(response.context['banners']) == list(Banner.objects.all())


