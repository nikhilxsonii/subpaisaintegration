from django.urls import path, include
from rest_framework.routers import DefaultRouter
from integration import views

router = DefaultRouter()
router.register(r'payment', views.PgView, basename='pg')

urlpatterns = [
    path('', views.index, name='pg-index'),                     
    path('api/pg/', include(router.urls)),                      
    path('initiate-payment/', views.initiate, name='initiate-payment'),
    path('response/', views.response, name='response'),
]
