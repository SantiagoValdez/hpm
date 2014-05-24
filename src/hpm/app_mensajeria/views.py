from django.shortcuts import render
from principal.models import Usuario
from principal.models import Mensaje
from principal.views import is_logged
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def indexMensaje(request):
    """
    Funcion: Panel principal de administracion de mensajes

    @param request: Objeto que se encarga de manejar las peticiones http.
    @return: Si el usuario se encuentra logueado retorna un objeto
            HttpResponse del template mensajes.html renderizado con el contexto
            {'usuario': u, 'lista': lista}. Sino, retorna un objeto
            HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        if request.method != 'POST':
        	destinatario = Usuario.objects.get(id=u['id'])
        	lista = Mensaje.objects.filter(receiver=destinatario)
        else:
            lista = Mensaje.objects.filter(
                username__startswith=request.POST['search'])

        usuarios = Usuario.objects.all()
        return render(request, 'mensajes.html', {'usuario': u, 'usuarios':usuarios,'lista': lista})

    else:
        return redirect('/login')

def nuevoMensaje(request):
    """
    Funcion: Se ocupa de crear un nuevo mensaje

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_sender: Identificador del usuario remitente.
    @param id_receiver: Identificador del usuario destinatario.
    @return: Si el usuario no esta logueado retorna un objeto HttpResponseRedirect
    	hacia '/login'. Si el metodo no es POST  retorna un objeto HttpResponseRedirect
    	hacia el indice de mensajes.
    """
    u = is_logged(request.session)

    if(u):

        if(request.method == 'POST'):

            if ('receiver' in request.POST and
                    'asunto' in request.POST and
                    'mensaje' in request.POST):

                remitente = Usuario.objects.get(id=u['id'])
                destinatario = Usuario.objects.get(id=request.POST['receiver'])

                mensaje = Mensaje()
                mensaje.sender = remitente
                mensaje.receiver = destinatario
                mensaje.asunto = request.POST['asunto']
                mensaje.mensaje = request.POST['mensaje']
                mensaje.estado = 'no leido'
                
                try:
                    mensaje.save()
                except Exception, e:
                    # Error al guardar
                    print e
                    messages.error(
                        request, 'Ocurrio un error al crear el mensaje. Verifique los campos e intente de nuevo.')

                # Se creo el mensaje correctamente
                messages.success(
                    request, u'El mensaje ha sido creado con exito! :)')

            else:
                messages.warning(
                    request, 'Olvido completar algunos campos obligatorios, intente de nuevo')

        return redirect('mensajes:index')

    else:
        return redirect('/login')

def eliminarMensaje(request, id_mensaje):
    """
    Funcion: Se ocupa de eliminar un mensaje

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id: id del mensaje a ser eliminado.
    @return: Si el usuario se encuentra logueado y el usuario dado es eliminado
            exitosamente retorna un objeto HttpResponseRedirect hacia el indice
            de mensajes. Sino, retorna un objeto HttpResponseRedirect hacia '/login'.
    """
    u = is_logged(request.session)

    if(u):

        Mensaje.objects.filter(id=id_mensaje).delete()
        Mensaje.save()

        messages.success(request, 'Se ha eliminado el mensaje exitosamente.')

        return redirect('mensajes:index')

    else:
        return redirect('/login')

def verMensaje(request, id_mensaje):

	u = is_logged(request.session)

	if(u):
		mensaje = Mensaje.objects.get(id=id_mensaje)

		if(mensaje.estado == 'no leido'):
			mensaje.estado = 'leido'

			try:
				mensaje.save()
			except Exception, e:
				#Error al guardar
				print e
				messages.error(request, 'Ocurrio un error al vizualizar el mensaje.')

		return render(request,'ver-mensaje.html', {'usuario':u, 'mensaje':mensaje})
	else:
		return redirect('/login')