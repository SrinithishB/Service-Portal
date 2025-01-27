from django.urls import path
from . import views
app_name='Service Portal'
urlpatterns = [
    path("",views.index,name="index"),
    path("customer/",views.cust_dash,name="customer"),
    path("provider/",views.serv_dash,name="provider"),
    path("request_detail/<int:pk>",views.request_details,name="request_details"),
    path("quote_submission/<int:pk>",views.quote_submission,name="quote_submission"),
    path('accept_quote/<int:quote_id>/', views.accept_quote, name='accept_quote'),
    path('cancel_request/<int:request_id>/', views.cancel_request, name='cancel_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('my-bids/', views.my_bids, name='my_bids'),
    path('mark_completed/<int:request_id>/', views.mark_completed, name='mark_completed'),
]
