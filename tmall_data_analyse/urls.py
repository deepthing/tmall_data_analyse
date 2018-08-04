"""tmall_data_analyse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from vis import views as visual

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', visual.index),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login/$', visual.login),
    url(r'^order/$',visual.order_vis),
    url(r'^fee/$',visual.fee_vis),
    url(r'^inv/$',visual.inv_vis),
    url(r'^load/$',visual.jump_to_load),
    url(r'^upload/$',visual.upload),
    url(r'^testd3/$',visual.testd3),
    url(r'^basics/$',visual.basics_vis),
    url(r'^export_vis/$',visual.export_vis),
    url(r'^excel_export/$',visual.excel_export),
    url(r'^export_order/$',visual.order_export),
    url(r'^excel_export2/$',visual.excel_export2),
    url(r'^loadcsv',visual.loadcsv),
    url(r'^UndoUpload/$',visual.UndoUpload),
    url(r'^load_data_to_db/$',visual.load_data_to_db),
    url(r'analyse_data/',visual.analyse_data),
    url(r'analyse_data_process/',visual.analyse_data_process),
    url(r'load_data_to_db_process/',visual.load_data_to_db_process),
    url(r'^test1_view/$',visual.test1_view),
    url(r'^get_bom/$',visual.get_bom_data),
    url(r'^update_bom_edit/$',visual.update_bom_edit),
    url(r'^add_bom/$', visual.add_bom),
    url(r'^update_stroage_table/$', visual.update_stroage_table),
    url(r'^update_fee_table/$', visual.update_fee_table),
]


