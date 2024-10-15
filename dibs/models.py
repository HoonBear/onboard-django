from django.db import models

# Create your models here.
class DibsGroup(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to="user.User", null=False, on_delete=models.CASCADE, related_name="user"
    )

    class Meta:
        db_table = 'dibs_group'
        get_latest_by = 'createdAt'
        ordering = ('id',)

        constraints = (

        )

class DibsDetail(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    dibsGroup = models.ForeignKey(
        to="DibsGroup", null=False, on_delete=models.CASCADE, related_name="dibsGroup"
    )
    product = models.ForeignKey(
        to="product.Product", null=False, on_delete=models.CASCADE, related_name="product"
    )

    class Meta:
        db_table = 'dibs_detail'
        get_latest_by = 'createdAt'
        ordering = ('id',)

        constraints = (

        )