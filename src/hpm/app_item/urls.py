from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    #url(r'^$', 'app_fase.views.indexFase', name = 'index'),
    #url(r'^fases/(?P<id>\d+)/$','app_fase.views.indexFase', name='index'),
    url(r'^(?P<id_fase>\d+)/$','app_item.views.indexItem', name='index'),
    url(r'^(?P<id_fase>\d+)/nuevo/(?P<id_tipo_item>\d+)/','app_item.views.nuevoItem', name='nuevo'),
    url(r'^(?P<id_fase>\d+)/eliminar/(?P<id_item>\d+)/$', 'app_item.views.eliminarItem', name='eliminar'),
    url(r'^(?P<id_fase>\d+)/modificar/(?P<id_item>\d+)/','app_item.views.modificarItem', name='modificar'),
    url(r'^(?P<id_fase>\d+)/revertir/(?P<id_item>\d+)/','app_item.views.revertirItem', name='revertir'),
    

    url(r'^get/(?P<id_item>\d+)/$','app_item.views.getItem', name='get'),

)