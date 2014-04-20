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
    
    url(r'^usuarios/', include('principal.urls')),

    url(r'^proyectos/', include('principal.urls')),
    
    url(r'^api/usuarios/', include('principal.urls')),
    #url(r'^api/usuarios/', 'principal.views.apiGetUsuarios'),
    #url(r'^api/usuario/(?P<id>\d+)/$', 'principal.views.apiGetUsuario'),

    url(r'^api/proyectos', include('principal.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
