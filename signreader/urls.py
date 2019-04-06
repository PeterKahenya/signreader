from django.contrib import admin
from django.urls import path
from add import views as addviews
from read import views as readviews
from train import views as trainviews
from .home import index

urlpatterns = [
    path('', index),

    path('add/', addviews.index),
    path('read/', readviews.index),
    path('train/', trainviews.index),

    path('admin/', admin.site.urls),
]