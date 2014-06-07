from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^mensajes/', include('app_mensajeria.urls', namespace='mensajes')),
    
    url(r'^usuarios/', include('app_usuario.urls', namespace='usuarios')),

    url(r'^proyectos/', include('app_proyecto.urls' , namespace='proyectos')),

    url(r'^fases/', include('app_fase.urls' , namespace='fases')),
    
    url(r'^roles/', include('app_rol.urls' , namespace='roles')),
    
    url(r'^comites/', include('app_comite.urls' , namespace='comites')),

    url(r'^tipoitem/', include('app_tipo_item.urls' , namespace='tipoitem')),

    url(r'^lineabase/', include('app_linea_base.urls' , namespace='lineasbase')),

    url(r'^item/', include('app_item.urls' , namespace='item')),

    url(r'^solicitud/', include('app_solicitud.urls' , namespace='solicitud')),

    # url(r'^api/usuarios/', include('principal.urls')),
    # #url(r'^api/usuarios/', 'principal.views.apiGetUsuarios'),
    # #url(r'^api/usuario/(?P<id>\d+)/$', 'principal.views.apiGetUsuario'),

    # url(r'^api/proyectos', include('principal.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
