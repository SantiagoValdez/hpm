from django.shortcuts import render
from principal.models import Proyecto, Usuario, Fase, LineaBase, Item, HistorialLineaBase
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
from django.contrib import messages
import datetime

# Create your views here.


def indexLineaBase(request, id_fase):
    """
    Funcion: Panel principal de administracion de las lineas base de la fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase del cual se visualizan sus lineas base.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template lineasbase.html renderizado con el contexto
            {'usuario': u, 'fase' : fase, 'lineasb': lineasb}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        if request.method != 'POST':
            fase = Fase.objects.get(id=id_fase)
            lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
        else:
            fase = Fase.objects.get(id=id_fase)
            lineasb = LineaBase.objects.filter(
                nombre__startswith=request.POST['search'])

        return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb})

    else:
        return redirect('/login')


def nuevaLineaBase(request, id_fase):
    """
    Funcion: Se ocupa de crear una nueva linea base

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase a la cual se le agregara una nueva linea base.
    @return: Si el usuario se encuentra logueado y si una nueva linea base
            es creada exitosamente retorna un objeto HttpResponse del template
            lineasbase.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Se creo la linea base con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)
    # Falta forma de agregar los items
    if (u):
        fase = Fase.objects.get(id=id_fase)
        lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
        if (request.method == 'POST'):

            if('nombre' in request.POST):
                user = Usuario.objects.get(id=request.session['usuario'])

                lb = LineaBase()
                lb.nombre = request.POST['nombre']
                lb.fase = fase
                lb.estado = 'inicial'
                lb.usuario = user
                #lb.nro = lineasb.last().nro + 1
                lb.nro = lineasb.count() + 1

                try:
                    lb.save()
                    historialLineaBase("crear", lb.id, user.id)

                except Exception, e:
                    if(lb.id):
                        lb.delete()

                    print e

                    lineasb = LineaBase.objects.filter(
                        fase=fase).order_by('nro')
                    return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

                lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
                return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Se creo la linea base con exito'})
            else:
                lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
                return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Ocurrio un error'})

        else:
            return redirect('lineabase:index', id_fase=id_fase)
    else:
        return redirect('/login')


def eliminarLineaBase(request, id_fase, id_lineabase):
    """
    Funcion: Se ocupa de eliminar una linea base de una fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase de la cual se elimina la linea base. Utilizado para
            renderizar el indice de las lineas base.
    @param id_lineabase: Identificador de la linea base a ser eliminada.
    @return: Si el usuario se encuentra logueado y la linea base es eliminada
            exitosamente retorna un objeto HttpResponseRedirect hacia el indice de lineas base de la
            correspondiente fase.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        LineaBase.objects.filter(id=id_lineabase).delete()

        # falta poner los item que forman parte a estado aprobado

        return redirect('lineasbase:index', id_fase=id_fase)

    else:
        return redirect('/login')


def modificarLineaBase(request, id_fase):
    """
    Funcion: Se ocupa de modificar una linea base de una determinada fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase cuya linea base sera modificada.
    @return: Si el usuario se encuentra logueado y si la linea base es
            modificada exitosamente retorna un objeto HttpResponse del template
            lineasbase.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Se modifico la linea base con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):
        fase = Fase.objects.get(id=id_fase)
        #lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
        if(request.method == 'POST'):
            if ('nombre' in request.POST and
                    'id' in request.POST):

                lb = LineaBase.objects.get(id=request.POST['id'])
                if (lb):
                    lb.nombre = request.POST['nombre']

                    try:
                        lb.save()
                        user = Usuario.objects.get(
                            id=request.session['usuario'])
                        historialLineaBase("modificar", lb.id, user.id)
                    except Exception, e:
                        lineasb = LineaBase.objects.filter(
                            fase=fase).order_by('nro')
                        return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

                    lineasb = LineaBase.objects.filter(
                        fase=fase).order_by('nro')
                    return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Se modifico la linea base con exito'})

                else:
                    lineasb = LineaBase.objects.filter(
                        fase=fase).order_by('nro')
                    return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Ocurrio un error'})
            else:
                lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
                return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Ocurrio un error'})

        return redirect('lineabase:index', id_fase=id_fase)

    else:
        return redirect('/login')


def liberarLineaBase(request, id_fase, id_lineabase):
    """
    Funcion: Se ocupa de liberar la linea base

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase a la que pertenece la linea base a liberarse.
    @param id_lineabase: Identificador de la linea base a liberarse.
    @return: Si el usuario se encuentra logueado y si la linea base es
            liberada exitosamente retorna un objeto HttpResponse del template
            lineasbase.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Linea de base liberada' }.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)
        lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')

        lb.estado = "liberada"
        lb.save()
        user = Usuario.objects.get(id=request.session['usuario'])
        historialLineaBase("liberar", lb.id, user.id)

        # Falta la varificacion de los item pertenecientes

        return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Linea de base liberada'})

    else:
        return redirect('/login')


def cerrarLineaBase(request, id_fase, id_lineabase):
    """
    Funcion: Se ocupa de cerrar la linea base

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase a la que pertenece la linea base a cerrarse.
    @param id_lineabase: Identificador de la linea base a cerrarse.
    @return: Si el usuario se encuentra logueado y si la linea base es
            cerrrada exitosamente retorna un objeto HttpResponse del template
            lineasbase.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Linea de base cerrada' }.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)
        lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')

        lb.estado = "valido"
        lb.save()
        user = Usuario.objects.get(id=request.session['usuario'])
        historialLineaBase("cerrar", lb.id, user.id)

        # Falta la varificacion de los item pertenecientes

        return render(request, 'lineasbase.html', {'usuario': u, 'fase': fase, 'lineasb': lineasb, 'mensaje': 'Linea de base cerrada'})

    else:
        return redirect('/login')


def historialLineaBase(operacion, id_lineabase, id_usuario):
    """
    Funcion: Se ocupa de registrar las operaciones realizadas a una linea base

    @param operacion: Operacion realizada sobre la linea base.
    @param id_lineabase: Identificador de la linea base sobre la cual se realizan
            las operaciones.
    @param usuario: Usuario que realizo las operacion sobre la linea base.
    """

    lb = LineaBase.objects.get(id=id_lineabase)
    #date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now()
    user = Usuario.objects.get(id=id_usuario)
    op = operacion

    hist = HistorialLineaBase()
    hist.fecha = date
    hist.operacion = op
    hist.lineabase = lb
    hist.usuario = user.username
    hist.save()

def indexHistorialLineaBase(request, id_fase, id_lineabase):
    """"""
    u = is_logged(request.session)
    if(u):
        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)

        return render(request,'historial-lineabase.html', {'usuario' : u, 'fase' : fase, 'linea_base' : lb})
    else:
        redirect('/login')

def itemLineaBase(request,id_fase,id_lineabase):
    
    u = is_logged(request.session)
    if(u):
        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)

        return render(request,'item-lineabase.html', {'usuario' : u, 'fase' : fase, 'linea_base' : lb})
    else:
        redirect('/login')

def agregarItemLineaBase(request, id_fase, id_lineabase):
    u = is_logged(request.session)
    if(u):

        if(request.method == 'POST'):
            id_item = request.POST['id_item']
            item = Item.objects.get(id=id_item)
            lb = LineaBase.objects.get(id=id_lineabase)
            user = Usuario.objects.get(id=request.session['usuario'])
            
            try:
                addItemLB(id_item,id_lineabase)
                historialLineaBase("item " + item.nombre + " agregado",lb.id,user.id)
                messages.success(request, 'Se agrego el item con exito.')
            except Exception, e:
                print e
                messages.error(request,'Ocurrio un error al agregar el item. Intente de nuevo.')
            

        return redirect('lineasbase:items', id_fase = id_fase, id_lineabase = id_lineabase)
    else:
        redirect('/login')

def removerItemLineaBase(request, id_fase, id_lineabase, id_item):
    u = is_logged(request.session)
    if(u):        
        
        try:
            item = Item.objects.get(id=id_item)
            lb = LineaBase.objects.get(id=id_lineabase)
            user = Usuario.objects.get(id=request.session['usuario'])
            deleteItemLB(id_item)
            historialLineaBase("item " + item.nombre + " elimanado",lb.id,user.id)
            messages.success(request, 'Se removio el item con exito.')
        except Exception, e:
            print e
            messages.error(request,'Ocurrio un error al remover el item. Intente de nuevo.')

        return redirect('lineasbase:items', id_fase = id_fase, id_lineabase = id_lineabase)
    else:
        redirect('/login')

def addItemLB(id_item, id_lb):
	#comprobar que se pueda
    with transaction.atomic():
        lb = LineaBase.objects.get(id=id_lb)
        item = Item.objects.get(id=id_item)

        item.linea_base = lb
        item.estado = 'final'
        item.save()

def deleteItemLB(id_item):
	with transaction.atomic():
		item = Item.objects.get(id=id_item)

		item.linea_base = None

		item.save()
