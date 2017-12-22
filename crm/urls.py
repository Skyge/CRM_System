from django.conf.urls import url
from . import views


#app_name = 'crm'

urlpatterns = [
    url(r'^$', views.index, name="sales_index"),
    url(r'^customers$', views.customer_list, name="customer_list"),
    url(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    url(r'^customer/registration/(\d+)/(\w+)/$', views.registration, name="registration"),
]
