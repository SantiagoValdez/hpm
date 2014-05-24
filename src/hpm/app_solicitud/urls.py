from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^(?P<id_fase>\d+)/$', 'app_solicitud.views.indexSolicitud', name='index'),
    url(r'^(?P<id_fase>\d+)/eliminar/(?P<id_solicitud>\d+)/$', 'app_solicitud.views.eliminarSolicitud', name='eliminar'),
    url(r'^(?P<id_fase>\d+)/nuevo','app_solicitud.views.nuevoSolicitud', name='nuevo'),
    url(r'^(?P<id_fase>\d+)/modificar','app_solicitud.views.modificarSolicitud', name='modificar'),
    url(r'^(?P<id_fase>\d+)/enviar/(?P<id_solicitud>\d+)/$','app_solicitud.views.enviarSolicitud', name='enviar'),
    url(r'^(?P<id_fase>\d+)/aprobar/(?P<id_solicitud>\d+)/$','app_solicitud.views.aprobarSolicitud', name='aprobar'),
    url(r'^(?P<id_fase>\d+)/rechazar/(?P<id_solicitud>\d+)/$','app_solicitud.views.rechazarSolicitud', name='rechazar'),

)