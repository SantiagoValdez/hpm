from principal.models import Proyecto
from principal.models import Usuario
from principal.models import Rol
from principal.models import Permiso
from principal.models import Comite
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
import datetime
# Create your views here.

def indexProyecto(request):
	"""  
	Funcion: Panel principal de administracion de proyectos

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el usuario se encuentra logueado retorna un objeto 
		HttpResponse del template proyectos.html renderizado con el contexto 
		{'usuario': u, 'lista': lista}. Sino, retorna un objeto 
		HttpResponseRedirect hacia '/login'. 
	"""

	u = is_logged(request.session)

	if( u ):
		usuarios = Usuario.objects.all()

		if request.method != 'POST' :
			lista = Proyecto.objects.all()
		else:
			lista = Proyecto.objects.filter(nombre__startswith = request.POST['search'])

		return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'usuarios' : usuarios})

	else : 
		return redirect('/login')


def eliminarProyecto(request, id):
	"""  
	Funcion: Se ocupa de eliminar un proyecto

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del proyecto a ser eliminado.
	@return: Si el usuario se encuentra logueado y el proyecto es eliminado
		exitosamente retorna un objeto HttpResponseRedirect hacia '/proyectos'.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'. 
	"""
	u = is_logged(request.session)

	if( u ):

		Proyecto.objects.filter(id=id).delete()

		return redirect('/proyectos')

	else :
		return redirect('/login')

def nuevoProyecto(request):
	"""  
	Funcion: Se ocupa de crear un nuevo proyecto

	@param request: Objeto que se encarga de manejar las peticiones http. 
	@return: Si el usuario se encuentra logueado y si un nuevo proyecto
		es creado exitosamente retorna un objeto HttpResponse del template
		proyectos.html renderizado con el contexto 
		{'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo proyecto con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		usuarios = Usuario.objects.all()
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and 
				'complejidad_total' in request.POST and  
				'administrador' in request.POST) :
					p = Proyecto()
					p.nombre = request.POST['nombre']  
					p.descripcion = request.POST['descripcion']  
					p.fecha_creacion = datetime.datetime.now()
					p.complejidad_total = request.POST['complejidad_total'] 
					p.estado = "no iniciado"

					try:
						p.save()
						adm = Usuario.objects.get(id=request.POST['administrador'])
						setAdministrador(p,adm)
						crearComite(p, adm)
						p.save()
					except Exception, e:
						if(p.id):
							p.delete()
						
						lista = Proyecto.objects.all()
						print e
						return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error, por favor verifique que el nombre es unico he intente de nuevo','usuarios' : usuarios})
					

					lista = Proyecto.objects.all()
					return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo proyecto con exito','usuarios' : usuarios})

			else:
				lista = Proyecto.objects.all()
				return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error','usuarios' : usuarios})


		return redirect('/proyectos')

	else :
		return redirect('/login')


def modificarProyecto(request):
	"""  
	Funcion: Se ocupa de modificar un proyecto

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el usuario se encuentra logueado y si el proyecto es 
		modificado exitosamente retorna un objeto HttpResponse del template
		proyectos.html renderizado con el contexto 
		{'usuario' : u, 'lista' : lista, 'mensaje' : 'Se modifico proyecto con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		usuarios = Usuario.objects.all()
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and 
				'fecha_creacion' in request.POST and 
				'complejidad_total' in request.POST and 
				'estado' in request.POST and 
				'id' in request.POST  ) :
					id = request.POST['id'] 
					p = Proyecto.objects.get(id=id)
					if ( p ):

						if (request.POST['estado'] == 'finalizado') :
							fasesFinalCon = controlProyectoFinalizado(p)

							if (fasesFinalCon ==  False) :
								lista = Proyecto.objects.all()
								return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Existen fases sin finalizar','usuarios' : usuarios})

						p.nombre = request.POST['nombre']  
						p.descripcion = request.POST['descripcion']  
						p.fecha_creacion = datetime.datetime.strptime(request.POST['fecha_creacion'], '%d/%m/%Y').date()
						p.complejidad_total = request.POST['complejidad_total'] 
						p.estado = request.POST['estado'] 
						try:
							p.save()
						except Exception, e:
							lista = Proyecto.objects.all()
							return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error','usuarios' : usuarios})
						

						lista = Proyecto.objects.all()
						return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se modifico proyecto con exito','usuarios' : usuarios})
					else :
						lista = Proyecto.objects.all()
						return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error','usuarios' : usuarios})
			else:
				lista = Proyecto.objects.all()
				return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error','usuarios' : usuarios})


		return redirect('/proyectos')

	else :
		return redirect('/login')

def setAdministrador(proyecto, administrador):
	"""
	Funcion: Encargada de establecer un usuario administrador a un
		proyecto.

	@param proyecto: El proyecto al cual se establece el usuario
		administrador.
	@param administrador: Usuario dado para ser asignado como
		administrador del proyecto dado.
	"""	
	rol = Rol()
	rol.nombre = "Administrador del Proyecto " + proyecto.nombre
	rol.proyecto = proyecto
	rol.descripcion = "Rol del administrador del proyecto " + proyecto.nombre
	rol.save()

	administrador.roles.add(rol)
	administrador.save()

def crearComite(proyecto, administrador):
	"""
	Funcion: Encargada de establecer el comite de solicitudes de cambio
		proyecto.

	@param proyecto: El proyecto al cual se establece el usuario
		administrador.
	@param administrador: Usuario dado para ser asignado como
		administrador del proyecto dado.
	"""

	comite = Comite()
	comite.proyecto = proyecto
	comite.save()
	comite.usuarios.add(administrador)
	comite.save()

def controlProyectoFinalizado(proyecto):

	fases = proyecto.fase_set.all()
	fasesFinalc = False

	for f in fases :
		if (f.estado == 'finalizada') :
			fasesFinalc = True
		elif (f.estado != 'finalizada') :
			fasesFinalc = False

	return fasesFinalc