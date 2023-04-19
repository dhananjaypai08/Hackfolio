from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create, name='create'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('list/', views.list, name='list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
