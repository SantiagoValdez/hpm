from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^proyecto/', 'app_proyecto.views.indexProyecto'),
    url(r'^proyecto/eliminar/(?P<id>\d+)/$', 'app_proyecto.views.eliminarProyecto'),
    url(r'^proyecto/nuevo','app_proyecto.views.nuevoProyecto'),
    url(r'^proyecto/modificar','app_proyecto.views.modificarProyecto'),
)