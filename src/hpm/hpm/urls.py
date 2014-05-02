from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HPM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#
#   url(r'^admin/', include(admin.site.urls)),
#)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','principal.views.home'),
    
    url(r'^login/', 'principal.views.login'),
    url(r'^logout/', 'principal.views.logout'),
    
    url(r'^usuarios/', include('app_usuario.urls', namespace='usuarios')),

    url(r'^proyectos/', include('app_proyecto.urls' , namespace='proyectos')),

    url(r'^fases/', include('app_fase.urls' , namespace='fases')),
    
    url(r'^roles/', include('app_rol.urls' , namespace='roles')),
    
    url(r'^comites/', include('app_comite.urls' , namespace='comites')),
    # url(r'^api/usuarios/', include('principal.urls')),
    # #url(r'^api/usuarios/', 'principal.views.apiGetUsuarios'),
    # #url(r'^api/usuario/(?P<id>\d+)/$', 'principal.views.apiGetUsuario'),

    # url(r'^api/proyectos', include('principal.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
