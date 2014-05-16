from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Fase

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

class FaseTest(TestCase):

	def test_eliminacion_proyecto(self):
		proyecto = crear_proyecto("Proyecto1", "Descripcion1", timezone.now(), 0, "no iniciado")
		id_proyecto = proyecto.id

		for n in range(4):
			nrofase = n + 1
			crear_fase("Fase" + str(nrofase), "Fase de " + str(proyecto.nombre), proyecto)

		fases = Fase.objects.filter(proyecto=proyecto).order_by('nro')
		self.assertEqual(fases.count(),4)
		p = Proyecto.objects.get(id=id_proyecto)
		p.delete()
		p.save()
		fases = Fase.objects.all()
		self.assertEqual(fases.count(),0)