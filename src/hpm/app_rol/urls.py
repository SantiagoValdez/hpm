from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^$', 'app_rol.views.indexRol', name='index'),
    url(r'^eliminar/(?P<id>\d+)/$', 'app_rol.views.eliminarRol', name='eliminar'),
    url(r'^nuevo','app_rol.views.nuevoRol', name='nuevo'),
    url(r'^modificar','app_rol.views.modificarRol', name='modificar'),
    url(r'^permisos/(?P<id>\d+)/$','app_rol.views.permisosRol', name='permisos')
)