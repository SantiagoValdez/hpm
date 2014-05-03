from principal.models import Usuario
from principal.models import Rol
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

def indexUsuario(request):
	"""  
	Funcion: Panel principal de administracion de usuarios

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el usuario se encuentra logueado retorna un objeto 
		HttpResponse del template usuarios.html renderizado con el contexto 
		{'usuario': u, 'lista': lista}. Sino, retorna un objeto 
		HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		if request.method != 'POST' :
			lista = Usuario.objects.all()
		else:
			lista = Usuario.objects.filter(username__startswith = request.POST['search'])

		return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista})

	else : 
		return redirect('/login')


def eliminarUsuario(request, id):
	"""  
	Funcion: Se ocupa de eliminar un usuario

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del usuario a ser eliminado.
	@return: Si el usuario se encuentra logueado y el usuario dado es eliminado
		exitosamente retorna un objeto HttpResponseRedirect hacia '/usuarios'.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		Usuario.objects.filter(id=id).delete()

		return redirect('/usuarios')

	else :
		return redirect('/login')

def nuevoUsuario(request):
	"""  
	Funcion: Se ocupa de crear un nuevo usuario

	@param request: Objeto que se encarga de manejar las peticiones http. 
	@return: Si el usuario se encuentra logueado y si un nuevo usuario
		es creado exitosamente retorna un objeto HttpResponse del template
		usuarios.html renderizado con el contexto 
		{'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo usuario con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'apellido' in request.POST and 
				'username' in request.POST and 
				'password' in request.POST and 
				'email' in request.POST and 
				'ci' in request.POST and
				'telefono' in request.POST  ) :
					user = Usuario()
					user.nombre = request.POST['nombre']  
					user.apellido = request.POST['apellido']  
					user.username = request.POST['username']  
					user.password = request.POST['password'] 
					user.email = request.POST['email'] 
					user.ci = request.POST['ci'] 
					user.telefono = request.POST['telefono']
					try:
						user.save()
					except Exception, e:
						lista = Usuario.objects.all()
						
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error, comprueba que el username sea unico'})
					

					lista = Usuario.objects.all()
					
					return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo usuario con exito'})

			else:
				lista = Usuario.objects.all()
				
				return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/usuarios')

	else :
		return redirect('/login')


def modificarUsuario(request):
	"""  
	Funcion: Se ocupa de modificar un usuario

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el usuario se encuentra logueado y si el proyecto es 
		modificado exitosamente retorna un objeto HttpResponse del template
		usuarios.html renderizado con el contexto 
		{'usuario' : u, 'lista' : lista, 'mensaje' : 'Se modifico usuario con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'apellido' in request.POST and 
				'username' in request.POST and 
				'password' in request.POST and 
				'email' in request.POST and 
				'ci' in request.POST and
				'telefono' in request.POST and
				'id' in request.POST  ) :
					id = request.POST['id'] 
					user = Usuario.objects.get(id=id)
					if ( user ):
						user.nombre = request.POST['nombre']  
						user.apellido = request.POST['apellido']  
						user.username = request.POST['username']  
						user.password = request.POST['password'] 
						user.email = request.POST['email'] 
						user.ci = request.POST['ci'] 
						user.telefono = request.POST['telefono']
						try:
							user.save()
						except Exception, e:
							lista = Usuario.objects.all()
							
							return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
						

						lista = Usuario.objects.all()
						
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se modifico usuario con exito'})
					else :
						lista = Usuario.objects.all()
						
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
			else:
				lista = Usuario.objects.all()
				
				return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/usuarios')

	else :
		return redirect('/login')

def rolUsuario(request,id):
	"""
	Funcion: Pantalla de adm de roles del usuario

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del usuario al cual se le asignara roles
	@return: Si el usuario se encuentra logueado y si el rol existe retorna un 
		objeto HttpResponse del template permisos.html renderizado con el contexto
		{'usuario' : u, 'user' : usuario, 'roles' : roles, 'mensaje' : 'Se modificaron los roles del usuario con exito :)'}
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'. 
	"""

	u = is_logged(request.session)

	if( u ):

		usuario = Usuario.objects.get(id=id)
		if(usuario):
			roles = Rol.objects.all()
			
			if (request.method == 'POST' ) :
				#lista = Rol.objects.filter(nombre__startswith = request.POST['search'])
				# tengo que anadir los permisos al rol
				print "dentro de post"
				

				print request.POST
				
				rids = []
				if( 'roles' in request.POST ):
					#Ids de los permisos
					rids = request.POST.getlist('roles')
				
				try:
					usuario.roles.clear()
					for r in rids:
						rol = Rol.objects.get(id=r)
						usuario.roles.add(rol)

					usuario.save()
					return render(request, 'roles-usuario.html', {'usuario' : u, 'user' : usuario, 'roles' : roles, 'mensaje' : 'Se modificaron los roles del usuario con exito :)'})
				except Exception, e:
					print e
					return render(request, 'roles-usuario.html', {'usuario' : u, 'user' : usuario, 'roles' : roles, 'mensaje' : 'Ocurrio un error al modificar los roles del usuario, intente de nuevo'})

			return render(request, 'roles-usuario.html', {'usuario' : u, 'user' : usuario, 'roles' : roles})
		else:
			return redirect('/usuarios')
	else : 
		return redirect('/login')