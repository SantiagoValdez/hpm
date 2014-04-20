from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^$', 'app_proyecto.views.indexProyecto', name = 'index'),
    url(r'^eliminar/(?P<id>\d+)/$', 'app_proyecto.views.eliminarProyecto', name='eliminar'),
    url(r'^nuevo','app_proyecto.views.nuevoProyecto', name='nuevo'),
    url(r'^modificar','app_proyecto.views.modificarProyecto', name='modificar'),
)