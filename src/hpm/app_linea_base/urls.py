from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    #url(r'^$', 'app_fase.views.indexFase', name = 'index'),
    #url(r'^fases/(?P<id>\d+)/$','app_fase.views.indexFase', name='index'),
    url(r'^(?P<id_fase>\d+)/$','app_linea_base.views.indexLineaBase', name='index'),
    url(r'^(?P<id_fase>\d+)/nuevo','app_linea_base.views.nuevaLineaBase', name='nuevo'),
    url(r'^(?P<id_fase>\d+)/eliminar/(?P<id_lineabase>\d+)/$', 'app_linea_base.views.eliminarLineaBase', name='eliminar'),
    url(r'^(?P<id_fase>\d+)/modificar','app_linea_base.views.modificarLineaBase', name='modificar'),
    url(r'^(?P<id_fase>\d+)/cerrar/(?P<id_lineabase>\d+)/$','app_linea_base.views.cerrarLineaBase', name='cerrar'),
    url(r'^(?P<id_fase>\d+)/liberar/(?P<id_lineabase>\d+)/$','app_linea_base.views.liberarLineaBase', name='liberar'),
    url(r'^(?P<id_fase>\d+)/historial/(?P<id_lineabase>\d+)/$','app_linea_base.views.indexHistorialLineaBase', name='historial'),
    url(r'^(?P<id_fase>\d+)/items/(?P<id_lineabase>\d+)/$','app_linea_base.views.itemLineaBase', name='items'),
    url(r'^(?P<id_fase>\d+)/item/add/(?P<id_lineabase>\d+)/$','app_linea_base.views.agregarItemLineaBase', name='agregarItem'),
    url(r'^(?P<id_fase>\d+)/item/remove/(?P<id_lineabase>\d+)/(?P<id_item>\d+)/$','app_linea_base.views.removerItemLineaBase', name='removerItem'),
)