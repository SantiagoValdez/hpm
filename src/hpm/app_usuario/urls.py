from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^$', 'app_usuario.views.indexUsuario', name='index'),
    url(r'^eliminar/(?P<id>\d+)/$', 'app_usuario.views.eliminarUsuario', name='eliminar'),
    url(r'^nuevo','app_usuario.views.nuevoUsuario', name='nuevo'),
    url(r'^modificar','app_usuario.views.modificarUsuario', name='modificar'),
)