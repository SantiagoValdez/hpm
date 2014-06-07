from principal.models import Fase
from principal.models import Item
from principal.models import VersionItem
from principal.models import AtributoItem
from principal.models import TipoItem
from principal.models import Relacion
from principal.models import ArchivoForm, Archivo
from principal.models import HistorialItem
from principal.models import Usuario
from principal.views import is_logged
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
import json
import datetime
from django.utils.timezone import utc
from django.db import transaction
from django.contrib import messages
# Create your views here.


def indexItem(request, id_fase):
    """
    Funcion: Panel principal de administracion de los items

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase del cual se visualizan sus items.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template item.html renderizado con el contexto
            {'usuario' : u, 'fase' : fase, 'lista' : lista}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        fase = Fase.objects.get(id=id_fase)

        if request.method != 'POST':
            lista = fase.item_set.all().filter(eliminado=False)
        else:
            lista = fase.item_set.all().filter(
                nombre__startswith=request.POST['search'], eliminado=False)

        return render(request, 'item.html', {'usuario': u, 'fase': fase, 'lista': lista})

    else:
        return redirect('/login')


def nuevoItem(request, id_fase, id_tipo_item):
    """
    Funcion: Se ocupa de crear una nueva linea base

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase a la cual se le agregara un nuevo item.
    @param id_tipo_item: Identificador del tipo item el cual se utiliza como base para
            crear el item.
    @return: Si no esta logueado el usuario retorna un objeto HttpResponseRedirect
            hacia '/login'.
    """

    u = is_logged(request.session)

    if (u):
        fase = Fase.objects.get(id=id_fase)
        tipo_item = TipoItem.objects.get(id=id_tipo_item)

        if (request.method == 'POST'):

            if('nombre' in request.POST and
                    'numero' in request.POST and
                    'complejidad' in request.POST and
                    'costo' in request.POST and
                    'prioridad' in request.POST):

                user = Usuario.objects.get(id=request.session['usuario'])

                atributos = {
                    'complejidad':  request.POST['complejidad'],
                    'costo':  request.POST['costo'],
                    'prioridad':  request.POST['prioridad']
                }

                for atributo in tipo_item.atributotipoitem_set.all():

                    valor = atributo.valor_por_defecto

                    if(atributo.nombre in request.POST):
                        valor = request.POST[atributo.nombre]

                    atributos[atributo.nombre] = valor

                try:
                    newItem(request.POST["nombre"], request.POST[
                            "numero"], fase.id, tipo_item.id, atributos)
                    historialItem("crear", fase.id, user.id)

                except Exception, e:

                    print e

                    return render(request, 'nuevo-item.html', {'usuario': u, 'fase': fase, 'tipo_item': tipo_item, 'mensaje': 'Ocurrio un error al crear el item. Verifique los datos.'})

                return redirect('item:index', id_fase)
            else:
                return render(request, 'nuevo-item.html', {'usuario': u, 'fase': fase, 'tipo_item': tipo_item, 'mensaje': 'Ocurrio un error al crear el item. Verifique los datos.'})

        # ON GET
        else:

            return render(request, 'nuevo-item.html', {'usuario': u, 'fase': fase, 'tipo_item': tipo_item})

            # return HttpResponse("Hola fase :" + str(id_fase) + " tipo " +
            # str(id_tipo_item))
    else:
        return redirect('/login')


def eliminarItem(request, id_fase, id_item):
    """
    Funcion: Se ocupa de eliminar un item de una fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase de la cual se elimina el item. Utilizado para
            renderizar el indice de los items.
    @param id_lineabase: Identificador del item a ser eliminado.
    @return: Si el usuario se encuentra logueado y el item es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia el indice de items de la
            correspondiente fase.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        deleteItem(id_item)

        return redirect('item:index', id_fase=id_fase)

    else:
        return redirect('/login')


def modificarItem(request, id_fase, id_item):
    """
    Funcion: Se ocupa de modificar un item de una determinada fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase cuyo item sera modificado.
    @param id_item: Identificador del item que sera modificado.
    @return: Si el usuario no se encuentra logueado, retorna un objeto HttpResponseRedirect
            hacia '/login'.
    """

    u = is_logged(request.session)

    if (u):
        fase = Fase.objects.get(id=id_fase)
        item = Item.objects.get(id=id_item)
        version = VersionItem.objects.get(id=item.id_actual)
        tipo_item = item.tipo_item

        if (request.method == 'POST'):

            if(	'complejidad' in request.POST and
                    'costo' in request.POST and
                    'prioridad' in request.POST and
                    'estado' in request.POST):

                atributos = {
                    'complejidad':  request.POST['complejidad'],
                    'costo':  request.POST['costo'],
                    'prioridad':  request.POST['prioridad'],
                    'estado':  request.POST['estado']
                }

                for atributo in tipo_item.atributotipoitem_set.all():

                    valor = atributo.valor_por_defecto

                    if(atributo.nombre in request.POST):
                        valor = request.POST[atributo.nombre]

                    atributos[atributo.nombre] = valor

                user = Usuario.objects.get(id=request.session['usuario'])

                try:
                    newVersion(id_item, atributos)
                    historialItem('modificar', item.id, user.id)

                except Exception, e:

                    print e

                    return render(request, 'modificar-item.html', {'usuario': u, 'fase': fase, 'item': item, 'version': version, 'tipo_item': tipo_item, 'mensaje': 'Ocurrio un error al modificar el item. Verifique los datos.'})

                return redirect('item:index', id_fase)
            else:
                print "Campos incompletos..."
                return render(request, 'modificar-item.html', {'usuario': u, 'fase': fase, 'item': item, 'version': version, 'tipo_item': tipo_item, 'mensaje': 'Ocurrio un error al modificar el item. Verifique los datos.'})

        # ON GET
        else:

            return render(request, 'modificar-item.html', {'usuario': u, 'fase': fase, 'item': item, 'version': version, 'tipo_item': tipo_item})

            # return HttpResponse("Hola fase :" + str(id_fase) + " tipo " +
            # str(id_tipo_item))
    else:
        return redirect('/login')


def revertirItem(request, id_fase, id_item):
    """
    Funcion:  Se encarga de revertir la version del item a una anterior

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_fase: Identificador de la fase cuyo item sera revertido a una version
            anterior.
    @param id_item: Identificador del item que sera revertido a una version anterior.
    @return: Si el usuario se encuentra logueado y el item es revertido
            exitosamente retorna un objeto HttpResponse del template revivir-item.html
            renderizado con el contexto
            {'usuario' : u,'fase' : fase, 'item' : item,  'mensaje' : 'Se cambio la version del item con exito.' }.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if (u):
        fase = Fase.objects.get(id=id_fase)
        item = Item.objects.get(id=id_item)

        if (request.method == 'POST'):

            if(	'id_version' in request.POST):

                id_version = request.POST['id_version']
                user = Usuario.objects.get(id=request.session['usuario'])
                try:
                    setVersionItem(id_item, id_version)
                    historialItem(
                        'revertir a' + str(id_version), id_item, user.id)

                except Exception, e:

                    print e

                    return render(request, 'revertir-item.html', {'usuario': u, 'fase': fase, 'item': item,  'mensaje': 'Ocurrio un error al revertir el item. Intente de nuevo'})

                item = Item.objects.get(id=id_item)
                return render(request, 'revertir-item.html', {'usuario': u, 'fase': fase, 'item': item,  'mensaje': 'Se cambio la version del item con exito.'})
            else:
                print "Campos incompletos..."
                return render(request, 'revertir-item.html', {'usuario': u, 'fase': fase, 'item': item,  'mensaje': 'Ocurrio un error al revertir el item. Intente de nuevo.'})

        # ON GET
        else:

            return render(request, 'revertir-item.html', {'usuario': u, 'fase': fase, 'item': item})
    else:
        return redirect('/login')


def relacionarItem(request, id_fase, id_item):
    u = is_logged(request.session)

    if(u):

        fase = Fase.objects.get(id=id_fase)
        item = Item.objects.get(id=id_item)

        # on post
        if request.method == 'POST':
            if(('sucesor' in request.POST or 'hijo' in request.POST) and
               'tipo' in request.POST):

                try:

                    id_antecesor = id_item
                    tipo = request.POST['tipo']
                    if(tipo == 'padre-hijo'):
                        id_sucesor = request.POST['hijo']
                    else:
                        id_sucesor = request.POST['sucesor']

                    item1 = Item.objects.get(id=id_antecesor)
                    item2 = Item.objects.get(id=id_sucesor)
                    user = Usuario.objects.get(id=request.session['usuario'])
                    newRelacionItems(id_fase, tipo, id_antecesor, id_sucesor)
                    messages.success(request, 'Se creo la relacion con exito.')
                    historialItem(
                        'relacionar ' + item1.nombre + ' y ' + item2.nombre, id_item, user.id)
                except Exception, e:
                    print e
                    messages.error(
                        request, 'No se pudo crear la relacion. Intente de nuevo.')

            else:
                messages.error(
                    request, 'No se pudo crear la relacion. Intente de nuevo.')

        # finalmente... siempre... siempre...
        lista = getRelacionesItem(id_item)
        return render(request, 'relacionar-item.html', {'usuario': u, 'fase': fase, 'item': item, 'lista': lista})

    else:
        return redirect('/login')


def removerRelacionItem(request, id_fase, id_item, id_relacion):
    print "Remover ... Relacion "
    try:
        relacion = Relacion.objects.get(id=id_relacion)
        item1 = Item.objects.get(id=id_item)
        item2 = Item.objects.get(id=relacion.sucesor.proxy.id)
        user = Usuario.objects.get(id=request.session['usuario'])
        deleteRelacion(id_relacion)
        messages.success(request, "Se elimino la relacion con exito")
        historialItem(
            'eliminar relacion con' + item2.nombre, item1.id, user.id)

    except Exception, e:
        print e
        messages.error(request, "No se pudo eliminar la relacion")

    return redirect('item:relacionar', id_fase=id_fase, id_item=id_item)


def getItem(request, id_tipo_item):
    """
    Funcion: Se ocupa de obtener los datos de un item

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_tipo_item: Identificador del tipo de item del item del cual se quiere obtener sus datos.
    @return: Retorna un objeto HttpResponse con los datos del item en formato json.
    """

    ti = Item.objects.get(id=id_tipo_item)

    dic = {}
    dic['nombre'] = ti.nombre
    dic['descripcion'] = ti.descripcion
    dic['codigo'] = ti.codigo

    listaAtributos = []
    for a in ti.atributotipoitem_set.all():
        listaAtributos.append(
            {'nombre': a.nombre, 'tipo': a.tipo, 'valor_por_defecto': a.valor_por_defecto})

    dic['atributos'] = listaAtributos

    print dic

    data = json.dumps(dic)

    return HttpResponse(data)


def newItem(nombre, numero, id_fase, id_tipo_item, atributos):
    """
    Funcion: Encargada de crear un nuevo item.

    @param nombre: Nombre del nuevo item.
    @param numero: Numero del nuevo item.
    @param id_fase: Identificador de la fase a la que pertenece el item.
    @param id_tipo_item: Identificador del tipo de item del item.
    @param atributos: Atributos del item.
    """

    with transaction.atomic():
        # Creamos el item
        item = Item()
        item.nombre = nombre
        item.numero = numero
        item.eliminado = False

        fase = Fase.objects.get(id=id_fase)
        tipo_item = TipoItem.objects.get(id=id_tipo_item)
        item.fase = fase
        item.tipo_item = tipo_item

        item.save()

        # Creamos la version
        version_item = VersionItem()
        version_item.version = item.version
        version_item.complejidad = atributos["complejidad"]
        version_item.costo = atributos["costo"]
        version_item.prioridad = atributos["prioridad"]
        version_item.estado = "inicial"

        # Finalmente relacionamos la version con el item
        version_item.proxy = item

        version_item.save()

        # Seteamos los atributos del tipo item
        atributos_tipo_item = tipo_item.atributotipoitem_set.all()

        for atributo_tipo_item in atributos_tipo_item:

            atributo_item = AtributoItem()
            atributo_item.valor = atributos[atributo_tipo_item.nombre]
            atributo_item.atributo_tipo_item = atributo_tipo_item
            atributo_item.save()

            version_item.atributos.add(atributo_item)

        # Guardamos la version de nuevo y actualizamos las versiones
        version_item.save()
        item.version = version_item.version
        item.id_actual = version_item.id
        item.save()


def newVersion(id_item, atributos):
    """
    Funcion: Encargada de crear una nueva version del item.

    @param id_item: Identificador del item del cual se creara una version nueva.
    @param atributos: Atributos de la nueva version del item.
    """

    with transaction.atomic():

        item = Item.objects.get(id=id_item)
        tipo_item = item.tipo_item
        # Creamos la version
        version_item = VersionItem()
        version_item.version = item.version
        version_item.complejidad = atributos["complejidad"]
        version_item.costo = atributos["costo"]
        version_item.prioridad = atributos["prioridad"]
        version_item.estado = atributos["estado"]

        # Finalmente relacionamos la version con el item
        version_item.proxy = item

        version_item.save()

        # Seteamos los atributos del tipo item
        atributos_tipo_item = tipo_item.atributotipoitem_set.all()

        for atributo_tipo_item in atributos_tipo_item:

            atributo_item = AtributoItem()
            atributo_item.valor = atributos[atributo_tipo_item.nombre]
            atributo_item.atributo_tipo_item = atributo_tipo_item
            atributo_item.save()

            version_item.atributos.add(atributo_item)

        # Guardamos la version de nuevo y actualizamos las versiones
        version_item.save()
        item.version = version_item.version
        item.id_actual = version_item.id
        item.save()


def setEstadoItem(id_item, estado):
    with transaction.atomic():

        item = Item.objects.get(id=id_item)
        version_actual = VersionItem.objects.get(id=item.id_actual)

        version_actual.estado = estado

        version_actual.save()
        item.version = version_actual.version
        item.save()


def setVersionItem(id_item, id_version):
    """
    Funcion: Encargada de establecer la version del item.

    @param id_item: Identificador del item al que se establecera la version.
    @param id_version: Identificador de la version.
    """

    with transaction.atomic():

        item = Item.objects.get(id=id_item)
        version_item = VersionItem.objects.get(id=id_version)

        # Realizo este cambio solo para cambiar el timestamp
        version_item.proxy = item

        version_item.save()
        item.version = version_item.version
        item.id_actual = version_item.id
        item.save()


def deleteItem(id_item):
    """
    Funcion: Encargada de eliminar el item.

    @param id_item: Identificador del item a ser eliminado.
    """
    item = Item.objects.get(id=id_item)
    item.eliminado = True
    item.save()


def newRelacionItems(id_fase, tipo, id_antecesor, id_sucesor):
    """
    Funcion: Encargada de crear una relacino entre items.

    @param id_fase: Identificador de la fase en donde se encuentra la relacion.
    @param tipo: Tipo de relacion.
    @param id_antecesor: Identificador del item antecesor en la relacion.
    @param id_sucesor: Identificador del item sucesor en la relacion.
    """

    print "Nueva relacion..."
    print "ID A:" + str(id_antecesor)
    print "ID S:" + str(id_sucesor)

    fase = Fase.objects.get(id=id_fase)
    item_antecesor = Item.objects.get(id=id_antecesor)
    item_sucesor = Item.objects.get(id=id_sucesor)

    for relacion in getRelacionesItem(id_antecesor):
        if(item_sucesor == relacion.sucesor.proxy):
            raise Exception("Ya posee esta relacion!")

    antecesor = VersionItem.objects.get(id=item_antecesor.id_actual)
    sucesor = VersionItem.objects.get(id=item_sucesor.id_actual)

    proyecto = fase.proyecto

    relacion = Relacion()
    relacion.fase = fase
    relacion.proyecto = proyecto
    relacion.sucesor = sucesor
    relacion.antecesor = antecesor
    relacion.tipo = tipo

    relacion.save()


def deleteRelacion(id_relacion):
    """
    Funcion: Encargada de eliminar la relacion entre items.

    @param id_relacion: Identificador de la relacion a ser eliminada.
    """
    print "Dentro de Delete Relacion id : " + str(id_relacion)
    relacion = Relacion.objects.get(id=id_relacion)
    relacion.delete()


def getRelacionesItem(id_item):
    relaciones = None
    try:
        item = Item.objects.get(id=id_item)
        print item
        version = VersionItem.objects.get(id=item.id_actual)
        print version
        antecesores = version.relacion_antecesor_set.all()
        print antecesores
        sucesores = version.relacion_sucesor_set.all()
        print sucesores

        relaciones = []
        relaciones += antecesores
        relaciones += sucesores
        print relaciones

    except Exception, e:
        print e

    return relaciones


def historialItem(operacion, id_item, id_usuario):
    """
    Funcion: Se ocupa de registrar las operaciones realizadas a un item

    @param operacion: Operacion realizada sobre la linea base.
    @param id_item: Identificador del item sobre el cual se realizan
            las operaciones.
    @param usuario: Usuario que realizo las operacion sobre la linea base.
    """

    item = Item.objects.get(id=id_item)
    date = datetime.datetime.now().utcnow().replace(tzinfo=utc)
    user = Usuario.objects.get(id=id_usuario)
    op = operacion

    hist = HistorialItem()
    hist.fecha = date
    hist.operacion = op
    hist.item = item
    hist.usuario = user.username
    hist.save()


def indexHistorialItem(request, id_fase, id_item):
    """"""
    u = is_logged(request.session)
    if(u):
        item = Item.objects.get(id=id_item)
        fase = Fase.objects.get(id=id_fase)

        return render(request, 'historial-item.html', {'usuario': u, 'fase': fase, 'item': item})
    else:
        redirect('/login')


def adjuntarArchivo(request, id_fase, id_item):
    print id_fase

#    if request.method == 'POST':
#        form = ArchivoForm(request.POST, request.FILES)
#        item = Item.objects.get(id=id_item)
#        if form.is_valid:
#            nuevoArchivo = Archivo(archivo=request.FILES['archivo'])
#           nuevoArchivo.save()
#            item.archivo = nuevoArchivo
#
#            return redirect('item:index', id_fase=id_fase)
#    else:
#        form = ArchivoForm()


def calcularImpacto(id_item):
    item = Item.objects.get(id=id_item)

    #print item
    version = VersionItem.objects.get(id=item.id_actual)
    #print version
    antecesores = version.relacion_antecesor_set.all()
    #print antecesores
    sucesores = version.relacion_sucesor_set.all()
    #print sucesores

    relaciones = []
    relaciones += antecesores
    relaciones += sucesores
    #print relaciones

    impacto = 0 + version.costo

    for r in relaciones:
        if(r.antecesor.id != version.id):
            v = VersionItem.objects.get(id=r.antecesor.id)
            impacto = impacto + v.costo

        if(r.sucesor.id != version.id):
            v = VersionItem.objects.get(id=r.sucesor.id)
            impacto = impacto + v.costo

    #print impacto
    return impacto
