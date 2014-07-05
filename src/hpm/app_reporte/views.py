# -*- coding: utf-8 -*-
from principal.models import Solicitud
from principal.models import Comite
from principal.models import Mensaje
from principal.models import Usuario
from principal.models import Proyecto
from principal.models import Fase
from principal.models import Item
from principal.models import VersionItem
from principal.views import is_logged
from app_item.views import setEstadoItem
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
import datetime
from django.db import transaction
from django.contrib import messages
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import get_template
from django.template import Context


def testInforme(request):
    u = Usuario.objects.all()
    template_src = "informe-test.html"
    context_dict = {
        'mensaje': 'Usuario o password incorrectos...', 'usuarios': u}

    return render_to_pdf(template_src, context_dict)


def render_to_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(
        StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'filename='+ filename +'.pdf'
        return response
    return HttpResponse('No se pudo generar el reporte : <pre>%s</pre>' % cgi.escape(html))


def reporteProyecto(request, id_proyecto):
    """
    Funcion: Generacion de informe de proyecto

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: El id del proyecto que compete al reporte.
    @return: reporte en pdf que contiene la lista de ítems de un proyecto dado, 
    agrupado por fases. Dentro de cada fase, por cada ítem se deberá visualizar su 
    codigo o id, descripción o nombre, nombre de tipo de item, nombre del item padre 
    (si lo tuviere), versión y costo.'.
    """

    u = is_logged(request.session)

    if(u):
        proyecto = Proyecto.objects.get(id=id_proyecto)

        #return render(request, 'reporte-proyecto.html',{'proyecto' : proyecto})
        return render_to_pdf('reporte-proyecto.html', { 'proyecto': proyecto }, 'reporte-proyecto-'+ proyecto.nombre)

    else:
        return redirect('/login')

def reporteSolicitudes(request, id_proyecto):
    """
    Funcion: Generacion de informe de solicitudes de cambio en un proyecto

    @param request: Objeto que se encarga de manejar las peticiones http.
    @param id_proyecto: El id del proyecto que compete al reporte.
    @return: reporte en pdf que el líder del proyecto debe poder obtener un 
    listado de todas las solicitudes de cambio de un proyecto dado mostrando 
    la línea base afectada, el usuario que realizó la solicitud, si el líder ya 
    votó o no; y si la solicitud fue aprobada, rechazada, ejecutada o sigue pendiente.'.
    """
    u = is_logged(request.session)

    if(u):
        proyecto = Proyecto.objects.get(id=id_proyecto)
        solicitudes = Solicitud.objects.filter(fase__proyecto__id=id_proyecto)

        #return render(request, 'reporte-solicitud.html',{'usuario':u, 'proyecto': proyecto, 'solicitudes' : solicitudes})
        return render_to_pdf('reporte-solicitud.html',{'usuario':u, 'proyecto': proyecto, 'solicitudes' : solicitudes},'reporte-solicitudes-'+proyecto.nombre)

    else:
        return redirect('/login')
