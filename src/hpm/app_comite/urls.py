from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^p/(?P<id_proyecto>\d+)/$', 'app_comite.views.indexComite', name = 'index'),
    url(r'^p/(?P<id_proyecto>\d+)/eliminar/(?P<id_usuario>\d+)/$', 'app_comite.views.eliminarComite', name='eliminar'),
    url(r'^p/(?P<id_proyecto>\d+)/nuevo/$','app_comite.views.nuevoComite', name='nuevo'),

)