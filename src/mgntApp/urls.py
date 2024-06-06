from django.urls import path
from . import views
from mgntApp.forms import MyPasswordresetForm, MyPasswordChangeForm, MySetPasswordForm

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('', views.dashBoard, name="dashboard"),
    path('user/', views.userPage, name= "user_page"), 

    path('account/', views.accountSettings, name= "account"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    #------------ (CREATE URLS) ------------
    path('create_order/', views.createOrder, name="create_order"),

    path('add_product/', views.addProduct, name="add_product"),

    path('create_customer/', views.createcustomer, name="create_customer"),


   
    #------------ (UPDATE URLS) ------------
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),


    #------------ (UPDATE URLS) ------------
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', 
	form_class=MyPasswordresetForm), name= "reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
	 form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
      name='password_reset_complete'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='accounts/changepassword.html', 
	form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
	
	path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/passwordchangedone.html'), name='passwordchangedone'),

]
