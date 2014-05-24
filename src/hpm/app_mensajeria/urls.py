from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^$', 'app_mensajeria.views.indexMensaje', name='index'),
    url(r'^eliminar/(?P<id_mensaje>\d+)/$', 'app_mensajeria.views.eliminarMensaje', name='eliminar'),
    url(r'^nuevo','app_mensajeria.views.nuevoMensaje', name='nuevo'),
    url(r'^ver/(?P<id_mensaje>\d+)/$', 'app_mensajeria.views.verMensaje', name='ver'),
    
)