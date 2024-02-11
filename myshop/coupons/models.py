from django.db import models
from django.core.validators import MinValueValidator, \
 MaxValueValidator

class Coupon(models.Model):
    code = models.CharField('Код купона', max_length=50, unique=True)
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действет до')
    discount = models.IntegerField('Скидка', validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Percentage value (0 to 100')
    active = models.BooleanField('Доступен')
    
    
    class Meta:
        verbose_name = 'Скидочный купон'
        verbose_name_plural = 'Скидочные купоны'

    def __str__(self):
        return self.code
