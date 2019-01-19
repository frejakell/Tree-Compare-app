from django.conf.urls import url
from django.urls import path
from . import views
 
urlpatterns= [
    url(r'^$', views.index, name='index'),
    url(r'^results/', views.Results, name='edit'),
    url(r'^split/', views.Results_split, name='split'),
    url(r'^results_Display/', views.Results_Display, name='results_c'),
    url(r'^HM_Plot/(?P<t1>[0-9]+)$', views.HeatMap,name='HM_Plot'),
    url(r'^Hist_plot/(?P<t1>[0-9]+)$', views.Hist,name='Hist_plot'),
    url(r'^MDS_Color/(?P<t1>[0-9]+)$', views.MDS_cluster,name='MDS_Color'),
    url(r'^MDS_text/(?P<t1>[0-9]+)$', views.MDS_text,name='MDS_text'),
    url(r'^viewer/tree1/(?P<t1>[0-9]+)$', views.Tree1,name='Tree1'),
    url(r'^viewer/$', views.TreeView, name='viewer'),
    
]
