from django.db import models

# Create your models here.
class User(models.Model):
    loginId = models.CharField(max_length=10, unique=True, help_text="로그인 아이디", db_comment="로그인 아이디")
    password = models.CharField(max_length=100, help_text="패스워드", db_comment="패스워드")
    name = models.CharField(max_length=100, help_text="이름", db_comment="이름")
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = False # true 면 추상, 테이블 안만듬
        managed = True # false 면 마이그레이션 안함
        proxy = False # true 면 하나의 테이블을 2개이상 모델로 나눠서 관리하고 싶을 떄

        db_table = 'user'
        get_latest_by = 'createdAt'
        ordering = ('id',)

        constraints = (
            models.UniqueConstraint(fields=("loginId",), name="unique_login_id"),
        )