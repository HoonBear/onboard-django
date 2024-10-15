# Generated by Django 5.1.2 on 2024-10-15 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "loginId",
                    models.CharField(
                        db_comment="로그인 아이디",
                        help_text="로그인 아이디",
                        max_length=10,
                        unique=True,
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        db_comment="패스워드", help_text="패스워드", max_length=100
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_comment="이름", help_text="이름", max_length=100
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("modifiedAt", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user",
                "ordering": ("id",),
                "get_latest_by": "createdAt",
                "abstract": False,
                "managed": True,
                "proxy": False,
                "constraints": [
                    models.UniqueConstraint(fields=("loginId",), name="unique_login_id")
                ],
            },
        ),
    ]
