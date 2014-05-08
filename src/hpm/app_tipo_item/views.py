from principal.models import Proyecto
from principal.models import Usuario
from principal.models import Fase
from principal.models import TipoItem
from principal.models import AtributoTipoItem
from principal.views import is_logged
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
import json

# Create your views here.

def indexTipoItem(request, id_fase):

	u = is_logged(request.session)

	if( u ):

		fase = Fase.objects.get(id=id_fase)
		lista = fase.tipoitem_set.all()
			
		return render(request, 'tipo_item.html', {'usuario' : u, 'fase' : fase, 'lista' : lista})

	else : 
		return redirect('/login')

def nuevoTipoItem(request, id_fase):

	u = is_logged(request.session)

	if (u):
		fase = Fase.objects.get(id=id_fase)
		
		if (request.method == 'POST'):
			
			if('nombre' in request.POST and
				'descripcion' in request.POST and
				'codigo' in request.POST ):
				ti = TipoItem()
				ti.nombre = request.POST['nombre']
				ti.descripcion = request.POST['descripcion']
				ti.codigo = request.POST['codigo']
				ti.fase = fase
				ti.proyecto = fase.proyecto
				
								
				try:
					ti.save()
					
				except Exception, e:

					print e
					lista = fase.tipoitem_set.all()
					return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error, verifique que el nombre y el codigo son unicos e intente de nuevo'})

				lista = fase.tipoitem_set.all()
				return render(request, 'tipo_item.html',{'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Se creo el tipo item con exito'})
			else:
				lista = fase.tipoitem_set.all()
				return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error'})

		else:
			return redirect('tipoitem:index', id_fase = id_fase)
	else:
		return redirect('/login')

def eliminarTipoItem(request, id_fase, id_tipo_item):

	u = is_logged(request.session)

	if( u ):

		TipoItem.objects.filter(id=id_tipo_item).delete()

		return redirect('tipoitem:index', id_fase = id_fase)

	else :
		return redirect('/login')

def modificarTipoItem(request, id_fase):

	u = is_logged(request.session)

	if( u ):
		fase = Fase.objects.get(id=id_fase)
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'descripcion' in request.POST and
				'codigo' in request.POST and
				'id' in request.POST) :
				 
				t = TipoItem.objects.get(id=request.POST['id'])
				if ( t ):
					t.nombre = request.POST['nombre']  
					t.descripcion = request.POST['descripcion']  
					t.codigo = request.POST['codigo']

					try:
						t.save()
					except Exception, e:
						lista = fase.tipoitem_set.all()
						return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error, verifique que el nombre y el codigo son unicos e intente de nuevo'})

					lista = fase.tipoitem_set.all()
					return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Se modifico el tipo item con exito'})


				else:
					lista = fase.tipoitem_set.all()
					return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error'})

			else:
				lista = fase.tipoitem_set.all()
				return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error. Verifique si completo los campos correctamente'})



		return redirect('tipoitem:index', id_fase = id_fase)

	else :
		return redirect('/login')


def importarTipoItem(request, id_fase):
	u = is_logged(request.session)

	if (u):
		fase = Fase.objects.get(id=id_fase)
		
		if (request.method == 'POST'):
			
			if('nombre' in request.POST and
				'descripcion' in request.POST and
				'codigo' in request.POST and
				'id-tipo' in request.POST ):
				
				ti = TipoItem()
				ti.nombre = request.POST['nombre']
				ti.descripcion = request.POST['descripcion']
				ti.codigo = request.POST['codigo']
				ti.fase = fase
				ti.proyecto = fase.proyecto
				
				
								
				try:
					ti.save()
					#Copiamos los Atributos del Original

					to = TipoItem.objects.get(id=request.POST['id-tipo'])

					for at in to.atributotipoitem_set.all():
						a = AtributoTipoItem()
						a.nombre = at.nombre
						a.tipo = at.tipo
						a.valor_por_defecto = at.valor_por_defecto

						ti.atributotipoitem_set.add(a)
					
				except Exception, e:
					if(ti.id):
						ti.delete()
					print e
					lista = fase.tipoitem_set.all()
					return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error, verifique que el nombre y el codigo son unicos e intente de nuevo'})

				lista = fase.tipoitem_set.all()
				return render(request, 'tipo_item.html',{'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Se importo el tipo item con exito'})
			else:
				lista = fase.tipoitem_set.all()
				return render(request, 'tipo_item.html', {'usuario' : u,'fase' : fase,'lista' : lista,'mensaje' : 'Ocurrio un error'})

		else:
			return redirect('tipoitem:index', id_fase = id_fase)
	else:
		return redirect('/login')


def getTipoItem(request,id_tipo_item):
	ti = TipoItem.objects.get(id=id_tipo_item)

	dic = {}
	dic['nombre'] = ti.nombre
	dic['descripcion'] = ti.descripcion
	dic['codigo'] = ti.codigo
	
	listaAtributos = []
	for a in ti.atributotipoitem_set.all() :
		listaAtributos.append( {'nombre' : a.nombre, 'tipo' : a.tipo, 'valor_por_defecto' : a.valor_por_defecto  } )

	dic['atributos'] = listaAtributos
		

	print dic

	data = json.dumps(dic)
	
	return HttpResponse(data)

###############################################
#	Atributos de Tipo Item 					  #
#											  #
#											  #
###############################################

def indexAtributoTipoItem(request, id_tipo_item):

	u = is_logged(request.session)

	if( u ):

		tipoitem = TipoItem.objects.get(id=id_tipo_item)
		print tipoitem
		lista = tipoitem.atributotipoitem_set.all()
			
		return render(request, 'atributo_tipo_item.html', {'usuario' : u, 'tipo_item' : tipoitem, 'lista' : lista})

	else : 
		return redirect('/login')

def nuevoAtributoTipoItem(request, id_tipo_item):

	u = is_logged(request.session)

	if (u):
		tipoitem = TipoItem.objects.get(id=id_tipo_item)
		
		if (request.method == 'POST'):
			
			if('nombre' in request.POST and
				'valor_por_defecto' in request.POST and
				'tipo' in request.POST ):
				a = AtributoTipoItem()
				a.nombre = request.POST['nombre']
				a.valor_por_defecto = request.POST['valor_por_defecto']
				a.tipo = request.POST['tipo']
				a.tipo_item = tipoitem
				
				
								
				try:
					a.save()
					
				except Exception, e:

					print e
					lista = tipoitem.atributotipoitem_set.all()
					return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

				lista = tipoitem.atributotipoitem_set.all()
				return render(request, 'atributo_tipo_item.html',{'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Se creo el atributo con exito'})
			else:
				lista = tipoitem.atributotipoitem_set.all()
				return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Ocurrio un error'})

		else:
			return redirect('tipoitem:indexAtributo', id_tipo_item = id_tipo_item)
	else:
		return redirect('/login')

def eliminarAtributoTipoItem(request, id_tipo_item, id_atributo_tipo_item):

	u = is_logged(request.session)

	if( u ):

		AtributoTipoItem.objects.filter(id=id_atributo_tipo_item).delete()

		return redirect('tipoitem:indexAtributo', id_tipo_item = id_tipo_item)

	else :
		return redirect('/login')

def modificarAtributoTipoItem(request, id_tipo_item):

	u = is_logged(request.session)

	if( u ):
		tipoitem = TipoItem.objects.get(id=id_tipo_item)
		if( request.method == 'POST' ):
			if ( 'nombre' in request.POST and 
				'valor_por_defecto' in request.POST and
				'tipo' in request.POST and
				'id' in request.POST) :
				 
				a = AtributoTipoItem.objects.get(id=request.POST['id'])
				if ( a ):
					a.nombre = request.POST['nombre']
					a.valor_por_defecto = request.POST['valor_por_defecto']
					a.tipo = request.POST['tipo']

					try:
						a.save()
					except Exception, e:
						lista = tipoitem.atributotipoitem_set.all()
						return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Ocurrio un error, verifique que el nombre es unico e intente de nuevo'})

					lista = tipoitem.atributotipoitem_set.all()
					return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Se modifico el atributo con exito'})


				else:
					lista = tipoitem.atributotipoitem_set.all()
					return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Ocurrio un error'})

			else:
				lista = tipoitem.atributotipoitem_set.all()
				return render(request, 'atributo_tipo_item.html', {'usuario' : u,'tipo_item' : tipoitem,'lista' : lista,'mensaje' : 'Ocurrio un error. Verifique si completo los campos correctamente'})



		return redirect('tipoitem:indexAtributo', id_tipo_item = id_tipo_item)

	else :
		return redirect('/login')
