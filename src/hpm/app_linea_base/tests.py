from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Fase, LineaBase

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

def crear_fase(nombre, descripcion, proyecto):
	"""
	Funcion: Encargada de crear una fase para realizacion de pruebas
	"""
	nrofases = Fase.objects.count() + 1
	f = Fase.objects.create(nro=nrofases, nombre=nombre, descripcion=descripcion, proyecto=proyecto)
		
	return f

def crear_lineabase(fase, nombre):
	"""
	Funcion: Encargada de crear una linea base para realizacion de pruebas
	"""
	nrolb = LineaBase.objects.count() + 1
	lb = LineaBase.objects.create(fase=fase, usuario=None, nombre=nombre, nro=nrolb, estado="inicial")

class lineabaseTest(TestCase):

	def test_eliminacion_fase(self):
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		id_proyecto = proyecto.id
		fase = crear_fase("Fase test", "Fase de " + str(proyecto.nombre), proyecto)
		id_fase = fase.id
		lb = crear_lineabase(fase, "lb test")


		f = Fase.objects.get(id=id_fase)
		f.delete()
		f.save()
		lbs = LineaBase.objects.all()
		self.assertEqual(lbs.count(),0)