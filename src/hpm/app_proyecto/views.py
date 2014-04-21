from principal.models import Proyecto
from principal.models import Usuario
from principal.models import Rol
from principal.models import Permiso
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
						p.save()
					except Exception, e:
						p.delete()
						lista = Proyecto.objects.all()
						print e
						return render(request, 'proyectos.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error','usuarios' : usuarios})
					

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

	rol = Rol()
	rol.nombre = "Administrador del Proyecto " + proyecto.nombre
	rol.proyecto = proyecto
	rol.descripcion = "Rol del administrador del proyecto " + proyecto.nombre
	rol.save()

	administrador.roles.add(rol)
	administrador.save()
