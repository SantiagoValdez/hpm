from django.shortcuts import render
from principal.models import Proyecto, Fase, LineaBase
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

def indexLineaBase(request, id_fase):
	"""
	Funcion: Panel principal de administracion de las lineas base de la fase

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id_fase: Identificador de la fase del cual se visualizan sus lineas base.
	@return: Si el usuario se encuentra logueado retorna un objeto 
		HttpResponse del template lineasbase.html renderizado con el contexto 
		{'usuario': u, 'fase' : fase, 'lineasb': lineasb}. Sino, retorna un objeto 
		HttpResponseRedirect hacia '/login'.
	"""

	u = is_logged(request.session)

	if( u ):

		fase = Fase.objects.get(id=id_fase)
		lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
			
		return render(request, 'lineasbase.html', {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb})
		
	else : 
		return redirect('/login')

def nuevaLineaBase(request, id_fase):
	"""  
	Funcion: Se ocupa de crear una nueva linea base

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id_fase: Identificador de la fase a la cual se le agregara una nueva linea base. 
	@return: Si el usuario se encuentra logueado y si una nueva linea base 
		es creada exitosamente retorna un objeto HttpResponse del template
		lineasbase.html renderizado con el contexto 
		{'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Se creo la linea base con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""

	u = is_logged(request.session)
	# Falta forma de agregar los items
	if (u):
		fase = Fase.objects.get(id=id_fase)
		lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
		if (request.method == 'POST'):
			
			if('nombre' in request.POST):
				lb = LineaBase()
				lb.nombre = request.POST['nombre']
				lb.fase = fase
				lb.estado = 'inicial'
				#lb.nro = lineasb.last().nro + 1 
				lb.nro = lineasb.count() + 1 
								
				try:
					lb.save()
					
				except Exception, e:
					if(lb.id):
						lb.delete()

					print e
					
					return render(request, 'lineasbase.html', {'usuario' : u,'fase' : fase,'lineasb' : lineasb,'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

				return render(request, 'lineasbase.html',{'usuario' : u,'fase' : fase,'lineasb' : lineasb,'mensaje' : 'Se creo la linea base con exito'})
			else:
				return render(request, 'lineasbase.html', {'usuario' : u,'fase' : fase,'lineasb' : lineasb,'mensaje' : 'Ocurrio un error'})

		else:
			return redirect('lineabase:index', id_fase = id_fase)
	else:
		return redirect('/login')

def eliminarLineaBase(request, id_fase, id_lineabase):
	"""  
	Funcion: Se ocupa de eliminar una linea base de una fase

	@param request: Objeto que se encarga de manejar las peticiones http.
	@param id_fase: Identificador de la fase de la cual se elimina la linea base. Utilizado para
		renderizar el indice de las lineas base.
	@param id_lineabase: Identificador de la linea base a ser eliminada.
	@return: Si el usuario se encuentra logueado y la linea base es eliminada
		exitosamente retorna un objeto HttpResponseRedirect hacia el indice de lineas base de la
		correspondiente fase.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'. 
	"""

	u = is_logged(request.session)

	if( u ):

		LineaBase.objects.filter(id=id_lineabase).delete()

		return redirect('lineabase:index', id_fase = id_fase)

	else :
		return redirect('/login')

def modificarLineaBase(request, id_fase):
	"""  
	Funcion: Se ocupa de modificar una linea base de una determinada fase

	@param request: Objeto que se encarga de manejar las peticiones http.
	@id_fase: Identificador de la fase cuya linea base sera modificada
	@return: Si el usuario se encuentra logueado y si la linea base es 
		modificada exitosamente retorna un objeto HttpResponse del template
		lineasbase.html renderizado con el contexto 
		{'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Se modifico la linea base con exito'}.
		Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
	"""

	u = is_logged(request.session)

	if( u ):
		fase = Fase.objects.get(id=id_fase)
		#lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and
				'id' in request.POST) :
				 
				lb = LineaBase.objects.get(id=request.POST['id'])
				if ( lb ):
					lb.nombre = request.POST['nombre']  
										
					try:
						lb.save()
					except Exception, e:
						lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
						return render(request, 'lineasbase.html', {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo' })
					
					lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
					return render(request, 'lineasbase.html', {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Se modifico la linea base con exito' })

				else:
					lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
					return render(request, 'lineasbase.html', {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Ocurrio un error' })
			else:
				lineasb = LineaBase.objects.filter(fase=fase).order_by('nro')
				return render(request, 'lineasbase.html', {'usuario' : u, 'fase' : fase, 'lineasb' : lineasb, 'mensaje' : 'Ocurrio un error' })


		return redirect('lineabase:index', id_fase = id_fase)

	else :
		return redirect('/login')