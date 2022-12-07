from django.urls import path

from copa.apps.spenn import views

urlpatterns = [
    path('spenn-callback/', views.spenn_callback, name="spenn_callback"),
]
