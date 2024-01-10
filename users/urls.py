from django.urls import path

from users import views

urlpatterns = [
    path("", views.homepage_view, name='homepage'),
    path("create-user/", views.create_user, name='create_user'),
    path('invoice/<int:invoice_id>/<int:user_id>/', views.generate_invoice, name='invoice'),
    path('save-data/', views.save_data, name='save_data'),
    path('search/', views.search_records, name='search_records'),
    path('update/', views.update_invoice, name='update_invoice'),
    path('add_product/', views.add_product, name='add_product'),

]
