from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    url(r'^usuarios/', include('app_usuario.urls')),
    #url(r'^usuario/eliminar/(?P<id>\d+)/$', 'principal.views.eliminarUsuario'),
    #url(r'^usuario/nuevo','principal.views.nuevoUsuario'),
    #url(r'^usuario/modificar','principal.views.modificarUsuario'),

    url(r'^proyectos/', include('app_proyecto.urls')),

    url(r'^api/usuarios/', 'principal.views.apiGetUsuarios'),
    url(r'^api/usuario/(?P<id>\d+)/$', 'principal.views.apiGetUsuario'),

    url(r'^api/proyectos/', 'principal.views.apiGetProyectos'),
    url(r'^api/proyecto/(?P<id>\d+)/$', 'principal.views.apiGetProyecto'),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)