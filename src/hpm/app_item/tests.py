from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Fase, LineaBase, Item, AtributoItem, TipoItem

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

def crear_item(nombre, numero, fase, tipoItem):
	"""
	Funcion: Encargada de crear un item para la realizacion de pruebas
	"""
	item = Item()
	item.nombre = nombre
	item.numero = numero
	item.eliminado = False
	item.version = None
	item.id_actual = 0
	item.fase = fase
	item.tipo_item = tipoItem

	return item

def crear_tipo_item(nombre, codigo, descripcion, proyecto, fase):
	"""
	Funcion: Encargada de crear un tipo de item para realizacion de pruebas
	"""
	ti = TipoItem.objects.create(nombre=nombre, codigo=codigo, 
								descripcion=descripcion, proyecto=proyecto,
								fase=fase
								)
	return ti

class itemTest(TestCase):

	def test_item_eliminacion_fase(self):

		pr = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		pr.save()
		fs = crear_fase("Fase test", "Fase de " + str(pr.nombre), pr)
		fs.save()
		ti = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", pr, fs)

		it = crear_item('item test', 1, fs, ti)
		it.save()

		fs.delete()
		fs.save()
		its = Item.objects.all()
		self.assertEqual(its.count(),0)

	def test_item_eliminacion_proyecto(self):

		pr = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		pr.save()
		fs = crear_fase("Fase test", "Fase de " + str(pr.nombre), pr)
		fs.save()
		ti = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", pr, fs)

		it = crear_item('item test', 1, fs, ti)
		it.save()

		pr.delete()
		pr.save()
		its = Item.objects.all()
		fss = Fase.objects.all()
		self.assertEqual(fss.count(),0)
		self.assertEqual(its.count(),0)
