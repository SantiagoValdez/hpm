from principal.models import Solicitud
from principal.models import Comite
from principal.models import Mensaje
from principal.models import Usuario
from principal.models import Proyecto
from principal.models import Fase
from principal.models import Item
from principal.models import VersionItem
from principal.views import is_logged
from app_item.views import setEstadoItem
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
import datetime
from django.db import transaction
from django.contrib import messages


def indexSolicitud(request, id_fase):
    """
    Funcion: Panel principal de administracion de Solicitudes

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: El id del proyecto al que pertenece el comite.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template solicitudes.html renderizado con el contexto
            {'usuario': u, 'lista': lista}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):
        fase = Fase.objects.get(id=id_fase)
        lista = Solicitud.objects.filter(fase=fase)
        return render(request, 'solicitudes.html', {'usuario': u, 'lista': lista, 'fase': fase})

    else:
        return redirect('/login')


def eliminarSolicitud(request, id_fase, id_solicitud):
    """
    Funcion: Se ocupa de eliminar un comite

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id: id del comite a ser eliminado.
    @return: Si el usuario se encuentra logueado y el comite es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia '/Solicitudes'.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        solicitud = Solicitud.objects.get(id=id_solicitud)

        try:
            solicitud.delete()
            messages.success(request, "Se elimino la solicitud.")
        except Exception, e:
            print e
            messages.error(request, "No se pudo eliminar la solicitud.")

        return redirect('solicitud:index', id_fase=id_fase)

    else:
        return redirect('/login')


def nuevoSolicitud(request, id_fase):
    """
    Funcion: Se ocupa de crear un nuevo comite

    @param request: Objeto que se encarga de manejar las peticiones http.
    @return: Si el usuario se encuentra logueado y si un nuevo comite
            es creado exitosamente retorna un objeto HttpResponse del template
            solicitudes.html renderizado con el contexto
            {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo comite con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        if(request.method == 'POST'):
            if ('accion' in request.POST and
                'nombre' in request.POST and
                'descripcion' in request.POST and
                'id_item' in request.POST):

                accion = request.POST['accion']
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                id_item = request.POST['id_item']
                id_usuario = u['id']

                try:
                    newSolicitud(
                        id_fase, id_usuario, id_item, nombre, descripcion, accion)
                    messages.success(
                        request, "Se creo la solicitud con exito.")
                except Exception, e:
                    print e
                    messages.error(request, "No se pudo crear la solicitud.")
            else:
                messages.success(
                    request, "No se pudo crear la solicitud. Verifique los datos.")

        return redirect('solicitud:index', id_fase=id_fase)

    else:
        return redirect('/login')


def modificarSolicitud(request, id_fase):
    """
    Funcion: Se ocupa de crear un nuevo comite

    @param request: Objeto que se encarga de manejar las peticiones http.
    @return: Si el usuario se encuentra logueado y si un nuevo comite
            es creado exitosamente retorna un objeto HttpResponse del template
            solicitudes.html renderizado con el contexto
            {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo comite con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        if(request.method == 'POST'):
            if ('accion' in request.POST and
                'nombre' in request.POST and
                'descripcion' in request.POST and
                'id_item' in request.POST and
                'id_solicitud' in request.POST):

                accion = request.POST['accion']
                nombre = request.POST['nombre']
                descripcion = request.POST['descripcion']
                id_item = request.POST['id_item']
                id_solicitud = request.POST['id_solicitud']

                try:
                    modifySolicitud(
                        id_solicitud, id_item, nombre, descripcion, accion)
                except Exception, e:
                    print e
                    messages.error(
                        request, "No se pudo modificar la solicitud.")

                messages.success(request, "Se modifco la solicitud con exito.")

            else:
                messages.error(
                    request, "No se pudo modificar la solicitud. Verifique los datos.")

        return redirect('solicitud:index', id_fase=id_fase)

    else:
        return redirect('/login')


def enviarSolicitud(request, id_fase, id_solicitud):

    u = is_logged(request.session)

    if(u):
        try:
            sendSolicitud(id_solicitud)
            messages.success(request, "Se envio la solicitud")
        except Exception, e:
            print e
            messages.error(request, "No se pudo enviar la solicitud.")

        return redirect('solicitud:index', id_fase=id_fase)
    else:
        return redirect('/login')


def aprobarSolicitud(request, id_fase, id_solicitud):
    """
    Funcion: Se ocupa de eliminar un comite

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id: id del comite a ser eliminado.
    @return: Si el usuario se encuentra logueado y el comite es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia '/Solicitudes'.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        try:
            id_usuario = u['id']

            votarSolicitud(id_solicitud, id_usuario, 1)

            messages.success(request, "Se emitio su voto con exito.")
        except Exception, e:
            print e
            messages.error(request, "No se pudo votar la solicitud.")

        return redirect('solicitud:index', id_fase=id_fase)

    else:
        return redirect('/login')


def rechazarSolicitud(request, id_fase, id_solicitud):
    """
    Funcion: Se ocupa de eliminar un comite

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id: id del comite a ser eliminado.
    @return: Si el usuario se encuentra logueado y el comite es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia '/Solicitudes'.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        try:
            id_usuario = u['id']

            votarSolicitud(id_solicitud, id_usuario, -1)

            messages.success(request, "Se emitio su voto con exito.")
        except Exception, e:
            print e
            messages.error(request, "No se pudo votar la solicitud.")

        return redirect('solicitud:index', id_fase=id_fase)

    else:
        return redirect('/login')


def newSolicitud(id_fase, id_usuario, id_item, nombre, descripcion, accion):

    with transaction.atomic():
        fase = Fase.objects.get(id=id_fase)
        proyecto = fase.proyecto
        usuario = Usuario.objects.get(id=id_usuario)
        item = Item.objects.get(id=id_item)
        comite = proyecto.comite_set.first()

        solicitud = Solicitud()
        solicitud.item = item
        solicitud.fase = fase
        solicitud.usuario = usuario
        solicitud.nombre = nombre
        solicitud.descripcion = descripcion
        solicitud.accion = accion
        solicitud.estado = 'inicial'
        solicitud.cantidad_votantes = len(comite.usuarios.all())
        solicitud.votos_negativos = 0
        solicitud.votos_positivos = 0
        solicitud.save()


def modifySolicitud(id_solicitud, id_item, nombre, descripcion, accion):

    with transaction.atomic():

        solicitud = Solicitud.objects.get(id=id_solicitud)
        item = Item.objects.get(id=id_item)
        solicitud.item = item
        solicitud.nombre = nombre
        solicitud.descripcion = descripcion
        solicitud.accion = accion
        solicitud.estado = 'inicial'

        solicitud.save()


def sendSolicitud(id_solicitud):

    with transaction.atomic():

        solicitud = Solicitud.objects.get(id=id_solicitud)
        fase = solicitud.fase
        proyecto = fase.proyecto
        usuario = solicitud.usuario
        item = solicitud.item
        comite = proyecto.comite_set.first()

        solicitud.estado = 'pendiente'

        solicitud.save()

        for user in comite.usuarios.all():
            mensaje = Mensaje()
            mensaje.sender = usuario
            mensaje.receiver = user
            mensaje.asunto = "Solicitud de Cambio Generada"
            mensaje.mensaje = "Se ha creado una solicitud de cambio para el item " + \
                item.nombre + " de la fase " + fase.nombre + \
                " en el proyecto" + proyecto.nombre + \
                ". Favor votar en la brevedad posible."
            mensaje.estado = "no leido"
            mensaje.save()


def votarSolicitud(id_solicitud, id_usuario, voto):

    print "Votar... " + str(voto)
    solicitud = Solicitud.objects.get(id=id_solicitud)
    usuario = Usuario.objects.get(id=id_usuario)

    if(usuario in solicitud.votantes.all()):
        raise Exception('Ya voto!')
        print "YA VOTO!"
    else:
        with transaction.atomic():

            solicitud.votantes.add(usuario)

            if(voto == 1):
                solicitud.votos_positivos += 1
            else:
                solicitud.votos_negativos += 1

            # Si los votos positivos son mayores a la mitad mas 1
            if(solicitud.cantidad_votantes / 2 + 1 <= solicitud.votos_positivos):
                solicitud.estado = 'aprobado'

            if(solicitud.cantidad_votantes / 2 + 1 <= solicitud.votos_negativos):
                solicitud.estado = 'rechazado'

            solicitud.save()

    ejecutarSolicitud(id_solicitud)


def ejecutarSolicitud(id_solicitud):
    print "EJECUTAR SOLCITUD"
    solicitud = Solicitud.objects.get(id=id_solicitud)

    if(solicitud.estado == 'aprobado'):
    	print "SE APRUEBA!"
        liberarItem(solicitud.item)

    if(solicitud.estado == 'rechazado'):
    	print "SE RECHAZA!"
        item = solicitud.item
        fase = item.fase
        proyecto = fase.proyecto
        m = Mensaje()
        m.sender = Usuario.objects.get(id=1)
        m.receiver = solicitud.usuario
        m.asunto = "Solicitud de Cambio Rechazada"
        m.mensaje = "Su solicitud de cambio para el item " + \
            item.nombre + " de la fase " + fase.nombre + \
            " en el proyecto" + proyecto.nombre + "Ha sido rechazada."
        m.estado = "no leido"
        m.save()


def liberarItem(item):
    with transaction.atomic():

    	setEstadoItem(item.id, "revision")

        lb = item.linea_base
        lb.estado = 'no valido'
        item.save()
        lb.save()
