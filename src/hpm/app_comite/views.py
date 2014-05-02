from principal.models import Comite
from principal.models import Usuario
from principal.models import Proyecto
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
import datetime

def indexComite(request, id_proyecto):
	"""  
	Funcion: Panel principal de administracion de comites

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id_proyecto: El id del proyecto al que pertenece el comite.
	@return: Si el usuario se encuentra logueado retorna un objeto 
		HttpResponse del template comites.html renderizado con el contexto 
		{'usuario': u, 'lista': lista}. Sino, retorna un objeto 
		HttpResponseRedirect hacia '/login'. 
	"""

	u = is_logged(request.session)

	if( u ):
		proyecto = Proyecto.objects.get(id = id_proyecto)
		comite = proyecto.comite_set.first()
		usuarios = Usuario.objects.all()
		lista = comite.usuarios.all()
		print "debug... pre render"
		return render(request, 'comites.html', {'usuario' : u, 'lista' : lista, 'usuarios' : usuarios, 'proyecto' : proyecto})

	else : 
		return redirect('/login')


def eliminarComite(request, id_proyecto, id_usuario):
	"""  
	Funcion: Se ocupa de eliminar un comite

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del comite a ser eliminado.
	@return: Si el usuario se encuentra logueado y el comite es eliminado
		exitosamente retorna un objeto HttpResponseRedirect hacia '/comites'.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'. 
	"""
	u = is_logged(request.session)

	if( u ):

		proyecto = Proyecto.objects.get(id = id_proyecto)
		comite = proyecto.comite_set.first()
		miembro = Usuario.objects.get(id=id_usuario)
		
		try:
			comite.usuarios.remove(miembro)
			comite.save()	
		except Exception, e:
			print e
			return redirect('comites:index', id_proyecto = id_proyecto)

		return redirect('comites:index', id_proyecto = id_proyecto)

	else :
		return redirect('/login')

def nuevoComite(request, id_proyecto):
	"""  
	Funcion: Se ocupa de crear un nuevo comite

	@param request: Objeto que se encarga de manejar las peticiones http. 
	@return: Si el usuario se encuentra logueado y si un nuevo comite
		es creado exitosamente retorna un objeto HttpResponse del template
		comites.html renderizado con el contexto 
		{'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo comite con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		usuarios = Usuario.objects.all()
		proyecto = Proyecto.objects.get(id = id_proyecto)
		comite = proyecto.comite_set.first()
		if( request.method == 'POST' ):
			if ( 'miembro' in request.POST ) :

					miembro = Usuario.objects.get(id=request.POST['miembro'])

					try:
						comite.usuarios.add(miembro)
						comite.save()
					except Exception, e:
												
						lista = comite.usuarios.all()
						print e
						return render(request, 'comites.html', {'usuario' : u, 'lista' : lista, 'usuarios' : usuarios, 'proyecto' : proyecto, "mensaje" : "Ocurrio un error al intentar agregar el miembro"})
					

					lista = comite.usuarios.all()
					return render(request, 'comites.html', {'usuario' : u, 'lista' : lista, 'usuarios' : usuarios, 'proyecto' : proyecto, "mensaje" : "Se agrego el miembro con exito. Recuerde que el numero de miembros debe ser impar."})

			else:
				lista = comite.usuarios.all()
				return render(request, 'comites.html', {'usuario' : u, 'lista' : lista, 'usuarios' : usuarios, 'proyecto' : proyecto, "mensaje" : "Ocurrio un error al intentar agregar el miembro"})


		return redirect('comites:index', id_proyecto = id_proyecto)

	else :
		return redirect('/login')


def crearComite(proyecto):
	print "hola"
