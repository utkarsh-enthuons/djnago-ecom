from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView
from .forms import LoginForm, UserPasswordChange, UserPasswordReset, UserSetPasswordForm

urlpatterns = [
    # path('', views.HomeView),
    # class based view URL define
    path('', views.HomeView.as_view(), name='hompage'),
    # path('product-detail/<int:prim_key>', views.product_detail, name='product-detail'),
    path('product-detail/<slug:prim_key>', views.ProductDetail.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('payment-done/', views.payment_done, name='payment-done'),
    path('pluscart/', views.pluscart, name='pluscart'),
    path('minuscart/', views.minuscart, name='minuscart'),
    path('removeCart/', views.removecart, name='removecart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='shopping/changepassword.html', form_class=UserPasswordChange, success_url='/passwodchangedone/'), name='passwordchange'),
    path('passwodchangedone/', auth_view.PasswordChangeView.as_view(template_name='shopping/passwordchangedone.html'), name='passwodchangedone'),
    path('product/', views.product, name='product'),
    path('product/<slug:slug>', views.product, name='product'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='shopping/login.html', authentication_form=LoginForm), name='login'),
    path('registration/', views.Registration.as_view(), name='customerregistration'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='shopping/password_reset.html', form_class=UserPasswordReset), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='shopping/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='shopping/password_reset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='shopping/password_reset_complete.html',), name='password_reset_complete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
