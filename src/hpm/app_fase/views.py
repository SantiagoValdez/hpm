from principal.models import Proyecto
from principal.models import Usuario
from principal.models import Fase
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers

# Create your views here.

def indexFase(request, id_proyecto):

	u = is_logged(request.session)

	if( u ):

		proyecto = Proyecto.objects.get(id=id_proyecto)
		if(proyecto):
			fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
			
			return render(request, 'fases.html', {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases})
		else:
			return redirect('/proyectos')
	else : 
		return redirect('/login')

def nuevaFase(request, id_proyecto):

	u = is_logged(request.session)

	if (u):
		proyecto = Proyecto.objects.get(id=id_proyecto)
		fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
		if (request.method == 'POST'):
			
			if('nombre' in request.POST and
				'descripcion' in request.POST ):
				f = Fase()
				f.nombre = request.POST['nombre']
				f.descripcion = request.POST['descripcion']
				f.proyecto = proyecto
				f.estado = 'inicial'
				f.nro = fases.count() + 1 
								
				try:
					f.save()
					
				except Exception, e:
					if(f.id):
						f.delete()

					print e
					return render(request, 'fases.html', {'usuario' : u,'proyecto' : proyecto,'fases' : fases,'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

				return render(request, 'fases.html',{'usuario' : u,'proyecto' : proyecto,'fases' : fases,'mensaje' : 'Se creo la fase con exito'})
			else:
				return render(request, 'fases.html', {'usuario' : u,'proyecto' : proyecto,'fases' : fases,'mensaje' : 'Ocurrio un error'})

		else:
			return redirect('/fases')
	else:
		return redirect('/login')

def eliminarFase(request, id_proyecto, id_fase):

	u = is_logged(request.session)

	if( u ):

		Fase.objects.filter(id=id_fase).delete()

		return redirect('fases:index', id_proyecto = id_proyecto)

	else :
		return redirect('/login')

def modificarFase(request, id_proyecto):

	u = is_logged(request.session)

	if( u ):
		proyecto = Proyecto.objects.get(id=id_proyecto)
		fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and
				'id' in request.POST) :
				 
				f = Fase.objects.get(id=request.POST['id'])
				if ( f ):
					f.nombre = request.POST['nombre']  
					f.descripcion = request.POST['descripcion']  
					
					try:
						f.save()
					except Exception, e:
						return render(request, 'fases.html', {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo' })
					
					return render(request, 'fases.html', {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Se modifico proyecto con exito' })

				else:

					return render(request, 'fases.html', {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Ocurrio un error' })
			else:
				return render(request, 'fases.html', {'usuario' : u, 'proyecto' : proyecto, 'fases' : fases, 'mensaje' : 'Ocurrio un error' })


		return redirect('fases:index', id_proyecto = id_proyecto)

	else :
		return redirect('/login')