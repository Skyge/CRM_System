from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crm/', include("crm.urls")),
    url(r'^account/login/$', views.account_login),
    url(r'^account/logout/$', views.account_logout, name="account_logout"),
    url(r'^student/', include("student.urls")),
    url(r'^king_admin/', include("king_admin.urls")),
    url(r'^$', views.index),
]