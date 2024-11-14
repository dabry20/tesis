from django.urls import path
from .views import detalle_examen, register, login_view, prediagnostico, historial, perfil
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('prediagnostico/', prediagnostico, name='prediagnostico'),
    path('historial/', historial, name='historial'),
    path('perfil/', perfil, name='perfil'),
    path('examen/<int:examen_id>/', detalle_examen, name='detalle_examen'),  # Agregar esta línea
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]