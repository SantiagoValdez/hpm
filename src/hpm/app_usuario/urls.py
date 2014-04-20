from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^usuarios/', 'app_usuario.views.indexUsuario'),
    url(r'^usuario/eliminar/(?P<id>\d+)/$', 'app_usuario.views.eliminarUsuario'),
    url(r'^usuario/nuevo','app_usuario.views.nuevoUsuario'),
    url(r'^usuario/modificar','app_usuario.views.modificarUsuario'),
)