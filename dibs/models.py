from django.db import models


# Create your models here.
class DibsGroup(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to="user.User", null=False, on_delete=models.CASCADE, related_name="dibGroups"
    )

    class Meta:
        db_table = "dibs_group"
        get_latest_by = "createdAt"
        ordering = ("id",)

        constraints = ()


class DibsDetail(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    dibsGroup = models.ForeignKey(
        to="dibs.DibsGroup",
        null=False,
        on_delete=models.CASCADE,
        related_name="dibsDetails",
    )

    product = models.ForeignKey(
        to="product.Product",
        null=False,
        on_delete=models.CASCADE,
        related_name="dibsDetails",
    )

    class Meta:
        db_table = "dibs_detail"
        get_latest_by = "createdAt"
        ordering = ("id",)
