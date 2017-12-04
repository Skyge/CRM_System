from django.conf.urls import url
from . import views

# app_name = 'crm'

urlpatterns = [
    url(r'^$', views.index, name="table_index"),
    url(r'^(\w+)/(\w+)$', views.display_table_objs, name="table_objs"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name="table_obj_change"),
]
