from principal.models import Proyecto
from principal.models import Usuario
from principal.models import Fase
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template import Context
import random
from django.contrib import messages



def indexFase(request, id_proyecto):
    """
    Funcion: Panel principal de administracion de las fases del proyecto

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: Identificador del proyecto del cual se visualizan sus fases.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template fases.html renderizado con el contexto
            {'usuario': u, 'proyecto' : proyecto, 'lista': lista}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):

        proyecto = Proyecto.objects.get(id=id_proyecto)
        if(proyecto):
            fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
            graph,colores = generarGrafo(id_proyecto)
            return render(request, 'fases.html', {'usuario': u, 'proyecto': proyecto, 'fases': fases, 'graph': graph, 'colores' : colores})
        else:
            return redirect('/proyectos')
    else:
        return redirect('/login')


def nuevaFase(request, id_proyecto):
    """
    Funcion: Se ocupa de crear una nueva fase

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: Identificador del proyecto al cual se le agregara una nueva fase.
    @return: Si el usuario se encuentra logueado y si una nueva fase
            es creada exitosamente retorna un objeto HttpResponse del template
            fases.html renderizado con el contexto
            {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Se creo la fase con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if (u):
        proyecto = Proyecto.objects.get(id=id_proyecto)
        fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
        if (request.method == 'POST'):

            if('nombre' in request.POST and
                    'descripcion' in request.POST):
                f = Fase()
                f.nombre = request.POST['nombre']
                f.descripcion = request.POST['descripcion']
                f.proyecto = proyecto
                f.estado = 'inicial'
                f.nro = numeroFase(proyecto)

                try:
                    f.save()
                    messages.success(request, "Se creo la fase con exito")
                except Exception, e:
                    if(f.id):
                        f.delete()
                    print e
                    messages.error(request, "Ocurrio un error al crear la fase")

                
            else:
                messages.error(request, "Ocurrio un error al crear la fase")
        return redirect('fases:index', id_proyecto=id_proyecto)
    else:
        return redirect('/login')


def eliminarFase(request, id_proyecto, id_fase):
    """
    Funcion: Se ocupa de eliminar una fase del proyecto

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: Identificador del proyecto del cual se elimina una fase. Utilizado para
            renderizar el indice de fases.
    @param id_fase: Identificador de la fase a ser eliminada.
    @return: Si el usuario se encuentra logueado y el proyecto es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia el indice de fases del
            correspondiente proyecto.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):
    	try:
	        Fase.objects.filter(id=id_fase).delete()
	        proyecto = Proyecto.objects.get(id=id_proyecto)
	        numeroFase(proyecto)
        	messages.success(request, "Se elimino la fase.")
        except Exception, e:
            print e
            messages.error(request, "No se pudo eliminar la fase.")
        
        return redirect('fases:index', id_proyecto=id_proyecto)

    else:
        return redirect('/login')


def modificarFase(request, id_proyecto):
    """
    Funcion: Se ocupa de modificar una fase de un determinado proyecto

    @param request: Objeto que se encarga de manejar las peticiones http.
    @id_proyecto: Identificador del proyecto cuya fase sera modificada.
    @return: Si el usuario se encuentra logueado y si la fase es
            modificada exitosamente retorna un objeto HttpResponse del template
            fases.html renderizado con el contexto
            {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Se modifico la fase con exito'}.
            Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """

    u = is_logged(request.session)

    if(u):
        proyecto = Proyecto.objects.get(id=id_proyecto)
        fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
        if(request.method == 'POST'):
            if ('nombre' in request.POST and
                    'descripcion' in request.POST and
                    'id' in request.POST):

                f = Fase.objects.get(id=request.POST['id'])
                if (f):
                    f.nombre = request.POST['nombre']
                    f.descripcion = request.POST['descripcion']

                    try:
                        f.save()
                    except Exception, e:
                        return render(request, 'fases.html', {'usuario': u, 'proyecto': proyecto, 'fases': fases, 'mensaje': 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

                    return render(request, 'fases.html', {'usuario': u, 'proyecto': proyecto, 'fases': fases, 'mensaje': 'Se modifico proyecto con exito'})

                else:

                    return render(request, 'fases.html', {'usuario': u, 'proyecto': proyecto, 'fases': fases, 'mensaje': 'Ocurrio un error'})
            else:
                return render(request, 'fases.html', {'usuario': u, 'proyecto': proyecto, 'fases': fases, 'mensaje': 'Ocurrio un error'})

        return redirect('fases:index', id_proyecto=id_proyecto)

    else:
        return redirect('/login')


def generarGrafo(id_proyecto):
    """
    Funcion: Encargada de graficar el grafo de un proyecto dado

    @param id_item: Identificador del proyecto del cual se graficara su grafo de relaciones.
    @return: Conjunto de nodos que conforman el grafo de relaciones en formato javascript.
    """
    # nodes:{foo:{color:"black", label:"foo"}, bar:{color:"green", label:"bar"}},
    # edges:{ foo: { bar: { }, baz:{ color: "blue", label: "hello"} } }
    #
    colores = {}
    js = " "

    proyecto = Proyecto.objects.get(id=id_proyecto)

    #Genera los nodos
    js += 'nodes:{'
    for fase in proyecto.fase_set.all():
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r())
        colores[fase.id] = color
        for item in fase.item_set.all():
            version = item.versionitem_set.filter(id=item.id_actual).first()
            if(version.estado != 'eliminado'):
                js += str(item.id) + \
                    ':{color:"' + color + '", label:"' + item.nombre + '"},'

    js += '}'  # fin de los nodos

    # Genera las relaciones
    js += ',edges:{'
    for relacion in proyecto.relacion_set.filter(eliminado = False):
        if(relacion.antecesor.proxy.id_actual == relacion.antecesor.id
            and relacion.sucesor.proxy.id_actual == relacion.sucesor.id):
            if(relacion.tipo == 'padre-hijo'):
                color = 'green'
            else:
                color = 'black'

            js += str(relacion.antecesor.proxy.id) + \
                ':{' + str(relacion.sucesor.proxy.id) + \
                ':{ color : "' + color + '"}' + '},'


    js += '}'  # fin arcos

    js += " "  # fin
    print colores
    return js,colores

def numeroFase(proyecto):
	n = 0
	for f in proyecto.fase_set.order_by('nro'):
		n = n + 1
		f.nro = n
		f.save()
	return n + 1