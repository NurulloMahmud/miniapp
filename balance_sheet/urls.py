from django.urls import path, include
from rest_framework import routers
from .views import (
    IncomeCategoryViewSet, ExpenseCategoryViewSet,
)


router = routers.DefaultRouter()
router.register(r'api/income-categories', IncomeCategoryViewSet)
router.register(r'api/expense-categories', ExpenseCategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]