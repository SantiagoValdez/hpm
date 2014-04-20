from principal.models import Usuario
from principal.models import Proyecto

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

def apiGetProyectos(request):
	proyectos = Proyecto.objects.all()
	data =  serializers.serialize("json", Proyecto.objects.all())
	return HttpResponse(data)

def apiGetProyecto(request, id):
	proyecto = Proyecto.objects.all().filter(id=id)
	data = serializers.serialize("json", proyecto)
	return HttpResponse(data)

def is_logged(session):
	if( 'usuario' in session ):
		return Usuario.objects.get(id=session['usuario'])
	else:
		return False