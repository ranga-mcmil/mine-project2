from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mine_mgt'

urlpatterns = [
   # post views
   path('', views.dashboard, name='dashboard'),
   path('payments/', views.payments, name='payments'),
   path('claim/<int:id>', views.claim_detail, name='claim_detail'),
   path('application/<int:id>', views.claim_application, name='claim_application'),
   path('accept/<int:id>', views.accept, name='accept'),
   path('apply/', views.apply, name='apply'),
   path('forfeited/<int:id>', views.forfeited, name='forfeited'),

   path('apply_forfeited/<int:id>', views.apply_forfeited, name='apply_forfeited'),
   path('add_payment/<int:id>', views.add_payment, name='add_payment'),
   path('claims_on_offer/', views.claims_on_offer, name='claims_on_offer'),


]