from django.urls import path
from mail import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('contact/', views.contact_list_page, name='contact_list'),
    path('contact_page/', views.contact_index, name='contact_list_page'),

    path('main_page/', views.main_page, name='main_page'),


    path('import_mail/', views.import_mail, name='import'),
    path('export_mail/', views.export_mail, name='export'),
    path('login/', views.login, name='login'),
    path('about_us/', views.about_us, name='about_us'),
    path('mail_list/', views.mail_list, name='mail_list'),
    path('home/', views.home_page, name='homepage'),

]

