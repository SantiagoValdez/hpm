from principal.models import Usuario
from principal.models import Proyecto
from principal.models import Rol
from principal.models import Permiso
from principal.models import LineaBase
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
import os.path
import datetime



def home(request):
	"""  
	Funcion: Genera la pagina principal

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el usuario se encuentra logueado retorna un objeto 
		HttpResponse del template home.html renderizado con el contexto 
		{'usuario': u}. Sino, retorna un objeto HttpResponseRedirect 
		hacia '/login'.
	"""
	u = is_logged(request.session)

	if( u ):

		return render_to_response('home.html',{'usuario' : u})
	else : 
		return redirect('/login')

def login(request):
	"""  
	Funcion: Formulario de Login

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Si el metodo utilizado en la solicitud es POST, y si existe
		un usuario retorna un objeto HttpResponseRedirect hacia '/'.
		Sino, retorna un objeto HttpResponse del template login.html 
		renderizado.
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

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Retorna un objeto HttpResponseRedirect hacia '/login'.
	"""
	del request.session['usuario']

	return redirect('/login')

def apiGetUsuarios(request):
	"""  
	Retorna la lista de usuarios en formato json

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Retorna un objeto HttpResponse con la lista de usuarios.
	"""
	usuarios = Usuario.objects.all()

	data = serializers.serialize("json", Usuario.objects.all())
	return HttpResponse(data)

def apiGetUsuario(request, id):
	"""  
	Retorna los detalles de un usuario en formato json

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del usuario del que se requiere los detalles.
	@return: Retorna un objeto HttpResponse con los detalles del usuario.
	"""
	usuario = Usuario.objects.all().filter(id=id)
	data = serializers.serialize("json", usuario)
	
	return HttpResponse(data)

def apiGetProyectos(request):
	"""
	Funcion: Devuelve la lista de proyectos en formato json.

	@param request: Objeto que se encarga de manejar las peticiones http.
	@return: Retorna un objeto HttpResponse con la lista de proyectos.
	"""
	proyectos = Proyecto.objects.all()
	data =  serializers.serialize("json", Proyecto.objects.all())
	return HttpResponse(data)

def apiGetProyecto(request, id):
	"""  
	Funcion: Devuelve los detalles de un proyecto en formato json.

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id: id del proyecto del que se requiere los detalles.
	@return: Retorna un objeto HttpResponse con los detalles del proyecto.
	"""
	proyecto = Proyecto.objects.all().filter(id=id)
	data = serializers.serialize("json", proyecto)
	return HttpResponse(data)

def is_logged(session):
	"""
	Funcion: Se encarga de verificar si el usuario se encuentra logueado.
		Y anexa los permisos y los roles del usuario.

	@param session: Objeto que almacena datos sobre la sesion actual.
	@return: Si el usuario se encuentra logueado retorna el usuario en
		en cuestion. Sino, retorna False.
	"""

	if( 'usuario' in session ):
		user =  Usuario.objects.get(id=session['usuario'])
		u = user.__dict__

		lista_permisos = []
		lista_roles = []
		for r in user.roles.all():
			lista_roles.append(r.nombre)
			for p in r.permisos.all():
				lista_permisos.append(p.nombre)

		u['permisos'] = lista_permisos
		u['roles'] = lista_roles
		
		if( user.destinatario.filter(estado='no leido') ):
			u['no_leido'] = len(user.destinatario.filter(estado='no leido'))

		return u

	else:
		return False

def historialLineaBase(operacion, id_lineabase, usuario):
    """
    Funcion: Se ocupa de registrar las operaciones realizadas a una

    @param operacion: Operacion realizada sobre la linea base.
    @param id_lineabase: Identificador de la linea base sobre la cual se realizan
            las operaciones.
    @param usuario: Usuario que realizo las operacion sobre la linea base.
    """

    lb = LineaBase.objects.get(id=id_lineabase)
    fasenombre = lb.fase.nombre

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_path = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_path, 'historial/lineabase/')
    name = os.path.join(path, "informe-" + fasenombre + "-lb-" + str(lb.id))

    with open(name, "a") as myfile:
        myfile.write("{0}\t{1}\t{2}\t{3}\n".format(
            date, operacion, lb.nombre, usuario.username))