from django.urls import path
from . import views

urlpatterns = [
    path("lobby/", views.lobby, name="lobby"),
    path("habitaciones/", views.habitaciones, name="habitaciones"),
    path("restaurante/", views.restaurante, name="restaurante"),
    path("tyc/", views.tyc, name="tyc"),
    path("login/", views.LoginUsuario.as_view(), name="login"),
    path("signup/", views.RegistroUsuario.as_view(), name="signup"),
    path("promociones/", views.promociones, name="promociones"),
    path("logout/", views.LogoutUsuario.as_view(), name="logout"),
    path('tienda/', views.tienda_hotel, name='tienda'),
    #RECUPERACION DE USUARIO
    path("auth/recuperar/", views.CustomPasswordResetView.as_view(), name='password_reset'),
    path("auth/recuperar/enviado/", views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path("auth/recuperar/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("auth/recuperar/completo/", views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),    
]