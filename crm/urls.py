from django.conf.urls import url
from . import views


#app_name = 'crm'

urlpatterns = [
    url(r'^$', views.index, name="sales_index"),
    url(r'^customers$', views.customer_list, name="customer_list"),
    url(r'^customer/(\d+)/enrollment/$', views.enrollment, name="enrollment"),
    url(r'^customer/registration/(\d+)/(\w+)/$', views.registration, name="registration"),
    url(r'^contract_review/(\d+)/$', views.contract_review, name="contract_review"),
    url(r'^enrollment_rejection/(\d+)/$', views.enrollment_rejection, name="enrollment_rejection"),
    url(r'^payment/(\d+)/$', views.payment, name="payment"),

]
