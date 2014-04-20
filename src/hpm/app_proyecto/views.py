from principal.models import Proyecto

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

def indexProyecto(request):
	"""  
	Funcion: Panel principal de administracion de proyectos
	"""
	if( 'proyecto' in request.session ):

		p = Proyecto.objects.get(id=request.session['proyecto'])


		if request.method != 'POST' :
			lista = Proyecto.objects.all()
		else:
			lista = Proyecto.objects.filter(nombre__startswith = request.POST['search'])

		return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista})

	else : 
		return redirect('/login')


def eliminarProyecto(request, id):
	"""  
	Funcion: Se ocupa de eliminar un proyecto
	"""
	if( 'proyecto' in request.session ):

		Proyecto.objects.filter(id=id).delete()

		return redirect('/proyectos')

	else :
		return redirect('/login')

def nuevoProyecto(request):
	"""  
	Funcion: Se ocupa de crear un nuevo proyecto
	"""
	if( 'proyecto' in request.session ):

		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and 
				'fecha_creacion' in request.POST and 
				'complejidad_total' in request.POST and 
				'estado' in request.POST  ) :
					p = Proyecto()
					p.nombre = request.POST['nombre']  
					u.descripcion = request.POST['descripcion']  
					u.fecha_creacion = request.POST['fecha_creacion']  
					u.complejidad_total = request.POST['complejidad_total'] 
					u.estado = request.POST['estado'] 
					try:
						p.save()
					except Exception, e:
						lista = Proyecto.objects.all()
						p = Proyecto.objects.get(id=request.session['proyecto'])
						return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
					

					lista = Proyecto.objects.all()
					p = Proyecto.objects.get(id=request.session['proyecto'])
					return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Se creo proyecto con exito'})

			else:
				lista = Proyecto.objects.all()
				p = Proyecto.objects.get(id=request.session['proyecto'])
				return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/proyectos')

	else :
		return redirect('/login')


def modificarProyecto(request):
	"""  
	Funcion: Se ocupa de modificar un proyecto
	"""
	if( 'proyecto' in request.session ):

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
						p.fecha_creacion = request.POST['fecha_creacion']  
						p.complejidad_total = request.POST['complejidad_total'] 
						p.estado = request.POST['estado'] 
						try:
							p.save()
						except Exception, e:
							lista = Proyecto.objects.all()
							p = Proyecto.objects.get(id=request.session['proyecto'])
							return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
						

						lista = Proyecto.objects.all()
						u = Proyecto.objects.get(id=request.session['proyecto'])
						return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Se modifico proyecto con exito'})
					else :
						lista = Proyecto.objects.all()
						p = Proyecto.objects.get(id=request.session['proyecto'])
						return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
			else:
				lista = Proyecto.objects.all()
				p = Proyecto.objects.get(id=request.session['proyecto'])
				return render(request, 'proyectos.html', {'proyecto' : p, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/proyectos')

	else :
		return redirect('/login')