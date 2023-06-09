from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns = [
    path('',views.home,name='home'),
    path('create_product/',views.createProduct,name='create'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),
    path('products/',views.products,name ='products'),
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logout,name='logout'),
    path('user/',views.userPage,name='user-page'),
    path('account/',views.accountSettings,name='account'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'),
         name='password_reset_complete'),

]

urlpatterns+=static(settings.MEDIA_ROOT, document_root =settings.MEDIA_ROOT)

'''
1 - Submit email form                                 //PasswordResetView.as_view()
2 - Email sent success message                        //PasswordResetDoneView.as_view()
3 - Link to password reset form                      //PasswordResetConfirmView.as_view()
4 - Password successfully changed                    //PasswordResetCompleteView.as_view()



'''