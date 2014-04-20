from principal.models import Usuario

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

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