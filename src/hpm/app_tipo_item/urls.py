from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recetario.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$','principal.views.home'),
    
    #url(r'^$', 'app_fase.views.indexFase', name = 'index'),
    #url(r'^fases/(?P<id>\d+)/$','app_fase.views.indexFase', name='index'),
    url(r'^(?P<id_fase>\d+)/$','app_tipo_item.views.indexTipoItem', name='index'),
    url(r'^(?P<id_fase>\d+)/nuevo','app_tipo_item.views.nuevoTipoItem', name='nuevo'),
    url(r'^(?P<id_fase>\d+)/eliminar/(?P<id_tipo_item>\d+)/$', 'app_tipo_item.views.eliminarTipoItem', name='eliminar'),
    url(r'^(?P<id_fase>\d+)/modificar','app_tipo_item.views.modificarTipoItem', name='modificar'),
    url(r'^(?P<id_fase>\d+)/importar','app_tipo_item.views.importarTipoItem', name='importar'),

    url(r'^atributos/(?P<id_tipo_item>\d+)/$','app_tipo_item.views.indexAtributoTipoItem', name='indexAtributo'),
    url(r'^atributos/(?P<id_tipo_item>\d+)/nuevo','app_tipo_item.views.nuevoAtributoTipoItem', name='nuevoAtributo'),
    url(r'^atributos/(?P<id_tipo_item>\d+)/eliminar/(?P<id_atributo_tipo_item>\d+)/$', 'app_tipo_item.views.eliminarAtributoTipoItem', name='eliminarAtributo'),
    url(r'^atributos/(?P<id_tipo_item>\d+)/modificar','app_tipo_item.views.modificarAtributoTipoItem', name='modificarAtributo'),
    
    url(r'^get/(?P<id_tipo_item>\d+)/$','app_tipo_item.views.getTipoItem', name='get'),

)