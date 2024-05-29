import pytest 
from shop.tests.conftest import *  
from django.core.exceptions import ValidationError



@pytest.mark.django_db
class TestModelBanner:
    def test_create_banner(self, client, test_banner):

        banner = Banner.objects.create(image=test_banner.image,
                                       advertisement_text=test_banner.advertisement_text,
                                       link=test_banner.link,
                                       is_active=test_banner.is_active)


        banner_pk = banner._get_pk_val()

      
        assert Banner.objects.filter(pk=banner_pk).count() == 1


        assert banner.image == "test.jpg"
        assert banner.advertisement_text == "Test_Banner"
        assert banner.link == '#'
        assert banner.is_active == True
        assert str(banner) == "Test_Banner"


