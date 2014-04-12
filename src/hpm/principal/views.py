from principal.models import Bebida
from principal.models import Usuario

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers


# Create your views here.

def lista_bebidas(request):
	bebidas = Bebida.objects.all()
	if( 'usuario' in request.session ):
		return render_to_response('home.html',{'lista' : bebidas})
	else : 
		return redirect('/login')



def home(request):
	if( 'usuario' in request.session ):

		u = Usuario.objects.get(id=request.session['usuario'])

		return render_to_response('home.html',{'usuario' : u})
	else : 
		return redirect('/login')

def login(request):
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
	del request.session['usuario']

	return redirect('/login')


def indexUsuario(request):
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
	if( 'usuario' in request.session ):

		Usuario.objects.filter(id=id).delete()

		return redirect('/usuarios')

	else :
		return redirect('/login')

def nuevoUsuario(request):
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

def apiGetUsuarios(request):
	usuarios = Usuario.objects.all()

	data = serializers.serialize("json", Usuario.objects.all())
	return HttpResponse(data)

def apiGetUsuario(request, id):
	usuario = Usuario.objects.all().filter(id=id)
	data = serializers.serialize("json", usuario)
	
	return HttpResponse(data)