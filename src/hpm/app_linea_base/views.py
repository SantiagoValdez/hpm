from django.shortcuts import render
from principal.models import Proyecto, Usuario, Fase, LineaBase, Item, HistorialLineaBase
from principal.models import Relacion, VersionItem
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
from django.contrib import messages
from django.db.models import Q
import datetime
from django.utils.timezone import utc

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

        lineab = LineaBase.objects.get(id=id_lineabase)
        items = Item.objects.filter(linea_base=lineab)
        for i in items:
            version = VersionItem.objects.get(id=i.id_actual)
            version.estado = 'aprobado'
            version.save()
        LineaBase.objects.filter(id=id_lineabase).delete()
        # El estado de una fase es 'con linea base' cuando la fase tiene una
        # linea base
        fase = Fase.objects.get(id=id_fase)
        lineasb = LineaBase.objects.filter(fase=fase)
        cantidad_lb = lineasb.count()
        if (cantidad_lb == 0):
            fase.estado = 'en desarrollo'
            fase.save()

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
    @param id_usuario: Usuario que realizo las operacion sobre la linea base.
    """

    lb = LineaBase.objects.get(id=id_lineabase)
    #date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now().utcnow().replace(tzinfo=utc)
    user = Usuario.objects.get(id=id_usuario)
    op = operacion

    hist = HistorialLineaBase()
    hist.fecha = date
    hist.operacion = op
    hist.lineabase = lb
    hist.usuario = user.username
    hist.save()


def indexHistorialLineaBase(request, id_fase, id_lineabase):
    """
    Funcion: Panel de visualizacion del historial de un item

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase al que pertenece el item.
    @param id_lineabase: Identificador de la linea base de la cual se visualiza su historial.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template historial-lineabase.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'linea_base' : lb}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)
    if(u):
        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)

        return render(request, 'historial-lineabase.html', {'usuario': u, 'fase': fase, 'linea_base': lb})
    else:
        redirect('/login')


def itemLineaBase(request, id_fase, id_lineabase):

    u = is_logged(request.session)
    if(u):
        lb = LineaBase.objects.get(id=id_lineabase)
        fase = Fase.objects.get(id=id_fase)

        return render(request, 'item-lineabase.html', {'usuario': u, 'fase': fase, 'linea_base': lb})
    else:
        redirect('/login')


def agregarItemLineaBase(request, id_fase, id_lineabase):
    u = is_logged(request.session)
    if(u):

        if(request.method == 'POST'):
            id_item = request.POST['id_item']
            item = Item.objects.get(id=id_item)
            lb = LineaBase.objects.get(id=id_lineabase)
            fase = Fase.objects.get(id=id_fase)
            user = Usuario.objects.get(id=request.session['usuario'])

            try:
                addItemLB(id_item, id_lineabase)
                historialLineaBase(
                    "item " + item.nombre + " agregado", lb.id, user.id)
                messages.success(request, 'Se agrego el item con exito.')
                fase.estado = 'con linea base'
                fase.save()
                estadoFinalFase(id_fase, id_lineabase)
            except Exception, e:
                print e
                messages.error(
                    request, 'Ocurrio un error al agregar el item. Intente de nuevo.')

        return redirect('lineasbase:items', id_fase=id_fase, id_lineabase=id_lineabase)
    else:
        redirect('/login')


def removerItemLineaBase(request, id_fase, id_lineabase, id_item):
    u = is_logged(request.session)
    if(u):

        try:
            item = Item.objects.get(id=id_item)
            lb = LineaBase.objects.get(id=id_lineabase)
            fase = Fase.objects.get(id=id_fase)
            lbs = fase.lineabase_set.all()
            user = Usuario.objects.get(id=request.session['usuario'])
            deleteItemLB(id_item)
            historialLineaBase(
                "item " + item.nombre + " eliminado", lb.id, user.id)
            messages.success(request, 'Se removio el item con exito.')

            condicion = False   # Todas las lineas base tienen 0 items
            
            for lb in lbs :
                cantidadItems = lb.item_set.all().count()
                if (cantidadItems == 0) :
                    print 'lb con 0 items'
                    condicion = True
                elif (cantidadItems > 0) :
                    print 'lb con > 0 items'
                    condicion = False

            if (condicion == True) :
                fase.estado = 'en desarrollo'
                fase.save()

        except Exception, e:
            print e
            messages.error(
                request, 'Ocurrio un error al remover el item. Intente de nuevo.')

        return redirect('lineasbase:items', id_fase=id_fase, id_lineabase=id_lineabase)
    else:
        redirect('/login')


def addItemLB(id_item, id_lb):
        # comprobar que se pueda
    with transaction.atomic():
        lb = LineaBase.objects.get(id=id_lb)
        item = Item.objects.get(id=id_item)
        version = VersionItem.objects.get(id=item.id_actual)

        item.linea_base = lb
        item.save()
        version.estado = 'final'
        version.save()


def deleteItemLB(id_item):
    with transaction.atomic():
        item = Item.objects.get(id=id_item)
    version = VersionItem.objects.get(id=item.id_actual)

    item.linea_base = None
    item.save()
    version.estado = 'aprobado'
    version.save()


def estadoFinalFase(id_fase, id_lineabase):

    faseActual = Fase.objects.get(id=id_fase)
    proyecto = faseActual.proyecto
    itemsFaseActual = Item.objects.filter(fase=faseActual)
    # Cantidad de items en la fase
    cantidad_itemsFaseActual = itemsFaseActual.count()
    # Cantidad de items en la fase que estan en una linea base
    cantidad_itemsFaseActualLb = 0
    # Condicion de que todos los items de la fase deben estar en una linea base
    faseFinalc1 = False
    faseFinalc2 = False     # Condicion la fase anterior finalizada

    for i in itemsFaseActual:
        version = VersionItem.objects.get(id=i.id_actual)
        if (version.estado == 'final' or version.estado == 'eliminado'):
            cantidad_itemsFaseActualLb += 1

    if (cantidad_itemsFaseActual == cantidad_itemsFaseActualLb):
        # Todos los items de la fase actual se encuentran en lineas base
        faseFinalc1 = True

    print faseFinalc1
    if (faseFinalc1 == True):

        cantidadFases = proyecto.fase_set.all().count()
        if (cantidadFases == 1):
            # Solo existe una fase entonces se puede finalizar la fase
            faseFinalc2 = True

        elif (cantidadFases > 1):
            # Si existen mas fases se verifica si la fase anterior esta
            # finalizada
            nroFaseActual = faseActual.nro
            fases = Fase.objects.filter(proyecto=proyecto)
            faseAnterior = fases.filter(
                nro__lt=nroFaseActual).order_by('nro').last()

            if (faseAnterior == None):
        # No existe una fase anterior por lo tanto la fase es la primera
                faseFinalc2 = True

            elif (faseAnterior.estado == 'finalizada'):
                # Existe una fase anterior
                faseFinalc2 = True

    print faseFinalc2
    if (faseFinalc2 == True):
        faseActual.estado = 'finalizada'
        faseActual.save()
        print faseActual.estado

# Si existen lineas base global
# Mejorar la seccion para hallar la fase anterior
# def estadoFinalFase(id_fase, id_lineabase):
#
#    faseActual = Fase.objects.get(id=id_fase)
#    lista_itemfase = faseActual.item_set.all()
#    cantidad_itemfaseActual = 0
#
#    proyecto = faseActual.proyecto
#    ultimaFase = Fase.objects.filter(proyecto=proyecto).order_by('nro').last()
#
#    if (faseActual == ultimaFase) :
#        ultimaFasec = True
#
#    for i in lista_itemfase :
#        version = VersionItem.objects.get(id=i.id_actual)
#        if (version.estado == 'aprobado' or version.estado == 'final') :
#            cantidad_itemfaseActual += 1
#
#    lineab = LineaBase.objects.get(id=id_lineabase)
#    lista_itemlb = lineab.item_set.all()
#    cantidad_itemlb = lista_itemlb.count()

    # Primera condicion es que la cantidad de item en la fase sea igual
    # a la cantidad de item que cuenta la linea base
    # entonces todos los items de la fase se encuentran dentro de la linea base
#    print cantidad_itemfaseActual
#    print cantidad_itemlb
#    if (cantidad_itemfaseActual == cantidad_itemlb) :

# faseFinalc1 = False     # Todos los items dentro de la lb y con sucesores
# faseFinalc2 = False     # La fase anterior finalizada

        # Comprobacion de si todos los items tienen sucesores
#        for i in lista_itemlb :
#            version = VersionItem.objects.get(id=i.id_actual)

#            if (ultimaFasec == False) :
                # Si no es la ultima fase se busca ademas que cumpla el tipo de relacion
                # antecesor-sucesor
#                relaciones = Relacion.objects.filter(antecesor=version,tipo='antecesor-sucesor')
#            elif (ultimaFasec == True) :
                # Si es la ultima fase, entonces solo existiran relaciones del tipo padre-hijo
                #
#                relaciones = Relacion.objects.filter(antecesor=version,tipo='padre-hijo')

#            cantidad_relaciones = relaciones.count()

#            if (cantidad_relaciones > 0) :

#                for r in relaciones :
#                    if (r.sucesor != None) :
#                        faseFinalc1 = True
#                    elif (r.sucesor == None) :
#                        faseFinalc1 = False
#        print faseFinalc1
#        if (faseFinalc1 == True) :
#            nroFaseActual = faseActual.nro
#            print nroFaseActual
#            if (nroFaseActual > 1) :
#                nroFaseAnterior = nroFaseActual - 1
#                print 'entro 1'
# Suponiendo que todas las fases tienen sus numeros sucesivos y ordenados
                # de forma ascendente
#                faseAnterior = Fase.objects.get(nro=nroFaseAnterior,proyecto=proyecto)
#                faseAnteriorEstado = faseAnterior.estado

#                if (faseAnteriorEstado == 'finalizada') :
#                    faseFinalc2 = True
#            elif (nroFaseActual == 1) :
#                print 'entro 2'
#                faseFinalc2 = True

#        print faseFinalc2
#        if (faseFinalc2 == True) :
#            print 'finalizada'
#            faseActual.estado = 'finalizada'
#            faseActual.save()
