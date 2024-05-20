from conftest import * 
from django.urls import reverse 



@pytest.mark.django_db
class TestBannerTagsView:
    def test_show_banner(self, test_banner, client):
        url = reverse('banner:banner')

        response = client.get(url)
        

        assert response.templates[0].name == 'banner.html' 
        assert response.status_code == 200 
        assert test_banner.advertisement_text == "Test_Banner"
        assert test_banner.image == "test.jpg"
        assert test_banner.is_active == True 


