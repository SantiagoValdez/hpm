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
    url(r'^(?P<id_fase>\d+)/relacion/(?P<id_item>\d+)/','app_item.views.relacionarItem', name='relacionar'),
    url(r'^(?P<id_fase>\d+)/relaciones/(?P<id_item>\d+)/remover/(?P<id_relacion>\d+)','app_item.views.removerRelacionItem', name='removerRelacion'),
    url(r'^(?P<id_fase>\d+)/adjuntar/(?P<id_item>\d+)','app_item.views.adjuntarArchivo', name='adjuntar'),
    url(r'^(?P<id_fase>\d+)/historial/(?P<id_item>\d+)/$','app_item.views.indexHistorialItem', name='historial'),
    url(r'^get/(?P<id_item>\d+)/$','app_item.views.getItem', name='get'),
    url(r'^getImpacto/(?P<id_item>\d+)/$','app_item.views.getImpactoItem', name='getImpacto'),
    url(r'^(?P<id_fase>\d+)/revivir/(?P<id_item>\d+)/$', 'app_item.views.revivirItem', name='revivir'),
    url(r'^(?P<id_fase>\d+)/aprobar/(?P<id_item>\d+)/$', 'app_item.views.aprobarItem', name='aprobar'),
)