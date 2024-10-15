from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = False # true 면 추상, 테이블 안만듬
        managed = True # false 면 마이그레이션 안함
        proxy = False # true 면 하나의 테이블을 2개이상 모델로 나눠서 관리하고 싶을 떄

        db_table = 'product'
        get_latest_by = 'createdAt'
        ordering = ('id',)

        constraints = (

        )