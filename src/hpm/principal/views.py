from principal.models import Bebida
from principal.models import Usuario

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers



def home(request):
	"""  
	Funcion: Genera la pagina principal
	"""
	if( 'usuario' in request.session ):

		u = Usuario.objects.get(id=request.session['usuario'])

		return render_to_response('home.html',{'usuario' : u})
	else : 
		return redirect('/login')

def login(request):
	"""  
	Funcion: Formulario de Login
	"""
	if ( request.method == 'POST' ):
		
		try:
			u = Usuario.objects.get(username=request.POST['username'], password=request.POST['password'])
			if ( u != None ):
				request.session['usuario'] = u.id
				return redirect('/')

		except Exception as e :
			return render(request, 'login.html', {'mensaje' : 'Usuario o password incorrectos...'})		
	else :
		return render(request, 'login.html')

def logout(request):
	"""  
	Funcion: Finaliza sesion
	"""
	del request.session['usuario']

	return redirect('/login')


def indexUsuario(request):
	"""  
	Funcion: Panel principal de administracion de usuarios
	"""
	if( 'usuario' in request.session ):

		u = Usuario.objects.get(id=request.session['usuario'])


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
	"""
	if( 'usuario' in request.session ):

		Usuario.objects.filter(id=id).delete()

		return redirect('/usuarios')

	else :
		return redirect('/login')

def nuevoUsuario(request):
	"""  
	Funcion: Se ocupa de crear un nuevo usuario
	"""
	if( 'usuario' in request.session ):

		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'apellido' in request.POST and 
				'username' in request.POST and 
				'password' in request.POST and 
				'email' in request.POST and 
				'ci' in request.POST and
				'telefono' in request.POST  ) :
					u = Usuario()
					u.nombre = request.POST['nombre']  
					u.apellido = request.POST['apellido']  
					u.username = request.POST['username']  
					u.password = request.POST['password'] 
					u.email = request.POST['email'] 
					u.ci = request.POST['ci'] 
					u.telefono = request.POST['telefono']
					try:
						u.save()
					except Exception, e:
						lista = Usuario.objects.all()
						u = Usuario.objects.get(id=request.session['usuario'])
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
					

					lista = Usuario.objects.all()
					u = Usuario.objects.get(id=request.session['usuario'])
					return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se creo usuario con exito'})

			else:
				lista = Usuario.objects.all()
				u = Usuario.objects.get(id=request.session['usuario'])
				return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/usuarios')

	else :
		return redirect('/login')


def modificarUsuario(request):
	"""  
	Funcion: Se ocupa de modificar un usuario
	"""
	if( 'usuario' in request.session ):

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
					u = Usuario.objects.get(id=id)
					if ( u ):
						u.nombre = request.POST['nombre']  
						u.apellido = request.POST['apellido']  
						u.username = request.POST['username']  
						u.password = request.POST['password'] 
						u.email = request.POST['email'] 
						u.ci = request.POST['ci'] 
						u.telefono = request.POST['telefono']
						try:
							u.save()
						except Exception, e:
							lista = Usuario.objects.all()
							u = Usuario.objects.get(id=request.session['usuario'])
							return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
						

						lista = Usuario.objects.all()
						u = Usuario.objects.get(id=request.session['usuario'])
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Se modifico usuario con exito'})
					else :
						lista = Usuario.objects.all()
						u = Usuario.objects.get(id=request.session['usuario'])
						return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})
			else:
				lista = Usuario.objects.all()
				u = Usuario.objects.get(id=request.session['usuario'])
				return render(request, 'usuarios.html', {'usuario' : u, 'lista' : lista, 'mensaje' : 'Ocurrio un error'})


		return redirect('/usuarios')

	else :
		return redirect('/login')


def apiGetUsuarios(request):
	"""  
	Retorna la lista de usuarios en formato json
	"""
	usuarios = Usuario.objects.all()

	data = serializers.serialize("json", Usuario.objects.all())
	return HttpResponse(data)

def apiGetUsuario(request, id):
	"""  
	Retorna los detalles de un usuario en formato json
	"""
	usuario = Usuario.objects.all().filter(id=id)
	data = serializers.serialize("json", usuario)
	
	return HttpResponse(data)