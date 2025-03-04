"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework.routers import SimpleRouter

from dibs.views import DibsDetailViewSet, DibsGroupViewSet
from product.views import ProductViewSet
from user.views import UserViewSet

router = SimpleRouter()

router.register("user", UserViewSet, basename="user")
router.register("product", ProductViewSet, basename="product")
router.register("dibs-group", DibsGroupViewSet, basename="dibs-group")
router.register("dibs-detail", DibsDetailViewSet, basename="dibs-detail")

urlpatterns = router.urls
