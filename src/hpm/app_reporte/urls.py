from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    #url(r'^(?P<id_fase>\d+)/$', 'app_reporte.views.indexSolicitud', name='index'),
    url(r'^proyecto/(?P<id_proyecto>\d+)/$', 'app_reporte.views.reporteProyecto', name='proyecto'),
    url(r'^solicitudes/(?P<id_proyecto>\d+)/$', 'app_reporte.views.reporteSolicitudes', name='solicitud'),
    #url(r'^(?P<id_fase>\d+)/nuevo','app_reporte.views.nuevoSolicitud', name='nuevo'),
    #url(r'^(?P<id_fase>\d+)/modificar','app_reporte.views.modificarSolicitud', name='modificar'),
    #url(r'^(?P<id_fase>\d+)/enviar/(?P<id_reporte>\d+)/$','app_reporte.views.enviarSolicitud', name='enviar'),
    #url(r'^(?P<id_fase>\d+)/aprobar/(?P<id_reporte>\d+)/$','app_reporte.views.aprobarSolicitud', name='aprobar'),
    #url(r'^(?P<id_fase>\d+)/rechazar/(?P<id_reporte>\d+)/$','app_reporte.views.rechazarSolicitud', name='rechazar'),

)