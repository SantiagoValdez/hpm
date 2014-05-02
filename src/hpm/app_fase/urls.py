from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    #url(r'^$', 'app_fase.views.indexFase', name = 'index'),
    #url(r'^fases/(?P<id>\d+)/$','app_fase.views.indexFase', name='index'),
    url(r'^(?P<id_proyecto>\d+)/$','app_fase.views.indexFase', name='index'),
    url(r'^(?P<id_proyecto>\d+)/nuevo','app_fase.views.nuevaFase', name='nuevo'),
    url(r'^(?P<id_proyecto>\d+)/eliminar/(?P<id_fase>\d+)/$', 'app_fase.views.eliminarFase', name='eliminar'),
    url(r'^(?P<id_proyecto>\d+)/modificar','app_fase.views.modificarFase', name='modificar'),
    
)