from principal.models import Rol
from principal.models import Proyecto
from principal.models import Permiso
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

def indexRol(request):
	"""  
	Funcion: Panel principal de administracion de roles
	"""
	u = is_logged(request.session)

	if( u ):

		proyectos = Proyecto.objects.all()
		
		if request.method != 'POST' :
			lista = Rol.objects.all()
		else:
			lista = Rol.objects.filter(nombre__startswith = request.POST['search'])

		return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'proyectos' : proyectos})

	else : 
		return redirect('/login')


def eliminarRol(request, id):
	"""  
	Funcion: Se ocupa de eliminar un rol
	"""
	u = is_logged(request.session)

	if( u ):

		Rol.objects.filter(id=id).delete()

		return redirect('/roles')

	else :
		return redirect('/login')

def nuevoRol(request):
	"""  
	Funcion: Se ocupa de crear un nuevo rol
	"""
	u = is_logged(request.session)

	if( u ):
		proyectos = Proyecto.objects.all()
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST ) :
					r = Rol()
					r.nombre = request.POST['nombre']  
					r.descripcion = request.POST['descripcion']  
					
					proyecto = None
					if('proyecto' in request.POST and request.POST['proyecto'] != "0"):
						proyecto = Proyecto.objects.get(id=request.POST['proyecto'])

					r.proyecto = proyecto

					try:
						r.save()
					except Exception, e:
						lista = Rol.objects.all()
						
						return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error', 'proyectos' : proyectos})
					

					lista = Rol.objects.all()
					
					return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo rol con exito', 'proyectos' : proyectos})

			else:
				lista = Rol.objects.all()
				
				return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error', 'proyectos' : proyectos})


		return redirect('/roles')

	else :
		return redirect('/login')


def modificarRol(request):
	"""  
	Funcion: Se ocupa de modificar un rol
	"""
	u = is_logged(request.session)

	if( u ):
		proyectos = Proyecto.objects.all()
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and
				'id' in request.POST ) :
					id = request.POST['id']
					r = Rol.objects.get(id=id)
					if(r):
						r.nombre = request.POST['nombre']  
						r.descripcion = request.POST['descripcion']  
						
						proyecto = None
						if('proyecto' in request.POST and request.POST['proyecto'] != "0"):
							proyecto = Proyecto.objects.get(id=request.POST['proyecto'])

						r.proyecto = proyecto

						try:
							r.save()
						except Exception, e:
							lista = Rol.objects.all()
							
							return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error', 'proyectos' : proyectos})
						

						lista = Rol.objects.all()
						
						return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo rol con exito', 'proyectos' : proyectos})
					else:
						lista = Rol.objects.all()
						return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error', 'proyectos' : proyectos})

			else:
				lista = Rol.objects.all()
				
				return render(request, 'roles.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error', 'proyectos' : proyectos})


		return redirect('/roles')

	else :
		return redirect('/login')

def permisosRol(request,id):
	"""
	Pantalla de adm de permisos del rol... ?
	"""

	u = is_logged(request.session)

	if( u ):

		rol = Rol.objects.get(id=id)
		if(rol):
			permisos = Permiso.objects.all()
			
			if (request.method == 'POST' ) :
				#lista = Rol.objects.filter(nombre__startswith = request.POST['search'])
				# tengo que anadir los permisos al rol
				print "dentro de post"
				

				print request.POST
				
				pids = []
				if( 'permisos' in request.POST ):
					#Ids de los permisos
					pids = request.POST.getlist('permisos')
				
				try:
					rol.permisos.clear()
					for p in pids:
						permiso = Permiso.objects.get(id=p)
						rol.permisos.add(permiso)

					rol.save()
					return render(request, 'permisos.html', {'usuario' : u, 'rol' : rol, 'permisos' : permisos, 'mensaje' : 'Se modificaron los permisos con exito :)'})
				except Exception, e:
					print e
					return render(request, 'permisos.html', {'usuario' : u, 'rol' : rol, 'permisos' : permisos, 'mensaje' : 'Ocurrio un error al modificar los permisos, intente de nuevo'})

			return render(request, 'permisos.html', {'usuario' : u, 'rol' : rol, 'permisos' : permisos})
		else:
			return redirect('/roles')
	else : 
		return redirect('/login')

