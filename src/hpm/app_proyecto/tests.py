from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.utils import timezone
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from principal.models import Proyecto
from principal.models import Rol
from principal.models import Permiso
from principal.models import Usuario

# Create your tests here.

def crear_proyecto(nombre, descripcion, fecha_creacion, complejidad_total, estado):
	"""
	Funcion: Encargada de crear un proyecto para realizacion de pruebas
	"""
	return Proyecto.objects.create(nombre=nombre, descripcion=descripcion,
								 fecha_creacion=fecha_creacion,
								 complejidad_total=complejidad_total,
								 estado=estado
								 )

def crear_rol(nombre, descripcion):
	"""
	Funcion: Encargada de crear un rol para realizacion de pruebas
	"""
	return Rol.objects.create(nombre=nombre, descripcion=descripcion)

def crear_permiso(nombre, valor):
	"""
	Funcion: Encargada de crear un permiso para la realizacion de pruebas
	"""
	return Permiso.objects.create(nombre=nombre, valor=valor)

def crear_usuario(username, password):
	"""
	Funcion: Encargada de crear un usuario para la realizacion de pruebas
	"""
	return Usuario.objects.create(username=username, password=password, nombre='ust1',
								apellido='ust1', telefono='0000000000', 
								ci=4100100, email='ts1@mail.com'
								)

class ProyectoTest(TestCase):

	def test_creacion_proyecto(self):
		"""
		Se comprueba que el proyecto es creado exitosamente
		"""
		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		tp = Proyecto.objects.get(nombre="proyectoTest")
		self.assertEqual(tp.nombre, "proyectoTest")

	def test_eliminacion_proyecto(self):
		"""
		Se comprueba que al eliminar el proyecto, todos los roles
		asociado al mismo tambien son eliminados
		"""
		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		p.save()
		r = crear_rol("Administrador proyectoTest", "rol de prueba")
		r.proyecto = p
		r.save()
		pr = crear_permiso("crear",0)
		r.permisos.add(pr)
		pr = crear_permiso("modificar",0)
		r.permisos.add(pr)

		Proyecto.objects.get(nombre="proyectoTest").delete()
		tp = Proyecto.objects.all()
		r = Rol.objects.all()
		self.assertEqual(len(tp), 0)
		self.assertEqual(len(r), 0)

	def test_conexion(self):

		#client = Client()
		usuario = crear_usuario('admin', 'admin')
		usuario.save()
		p = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		p.save()
		res = self.client.post('/login/',{'username':'admin','password':'admin'})
		tsession = self.client.session
		print 'data'
		print tsession
		print tsession['usuario']
		print res
		self.assertEqual(tsession['usuario'], 1)
		res =  self.client.get('/proyectos/')
		self.assertContains(res,"proyectoTest")
		self.assertEqual(res.status_code, 200)
