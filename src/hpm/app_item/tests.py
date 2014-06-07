from django.test import TestCase, TransactionTestCase
from django.db import IntegrityError

# Create your tests here.

from django.test import TestCase
from django.utils import timezone
from principal.models import Proyecto, Fase, LineaBase, Item, AtributoItem, TipoItem, VersionItem, Relacion
from app_item.views import newItem, deleteItem, newVersion, setVersionItem, setEstadoItem
from app_item.views import newRelacionItems, deleteRelacion, getRelacionesItem, getAntecesoresItem
from app_item.views import getSucesoresItem
from app_item.views import getItem, getImpactoItem

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
		ti.save()

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
		ti.save()

		it = crear_item('item test', 1, fs, ti)
		it.save()

		pr.delete()
		pr.save()
		its = Item.objects.all()
		fss = Fase.objects.all()
		self.assertEqual(fss.count(),0)
		self.assertEqual(its.count(),0)

	def test_newItem(self):

		prt = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		prt.save()
		fst = crear_fase("Fase test", "Fase de " + str(prt.nombre), prt)
		fst.save()
		ti = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", prt, fst)
		ti.save()

		atributos = {'complejidad':2,'costo':4,'prioridad':1}

		newItem("item t",1,fst.id,ti.id,atributos)

		item = Item.objects.get(nombre="item t")
		self.assertEqual(item.nombre, "item t")

	def test_delItem(self):
		prt = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		prt.save()
		fst = crear_fase("Fase test", "Fase de " + str(prt.nombre), prt)
		fst.save()
		ti = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", prt, fst)
		ti.save()

		atributos = {'complejidad':2,'costo':4,'prioridad':1}

		newItem("item t",1,fst.id,ti.id,atributos)

		item = Item.objects.get(nombre="item t")
		self.assertEqual(item.nombre, "item t")
		deleteItem(item.id)
		items = Item.objects.all()
		self.assertEqual(items.count(),1)
		item = Item.objects.get(nombre="item t")
		self.assertEqual(item.eliminado, True)

	def test_relItem(self):
		prt = crear_proyecto("proyectoTest","Prueba de test.py", timezone.now(), 0, "no iniciado")
		prt.save()
		fst = crear_fase("Fase test", "Fase de " + str(prt.nombre), prt)
		fst.save()
		ti = crear_tipo_item("tipo item test", "testcod", "descripcion ti test", prt, fst)
		ti.save()

		atributos = {'complejidad':2,'costo':4,'prioridad':1}

		newItem("item t1",1,fst.id,ti.id,atributos)
		item1 = Item.objects.get(nombre="item t1")
		vitem1 = VersionItem.objects.get(proxy=item1)
		newItem("item t2",2,fst.id,ti.id,atributos)
		item2 = Item.objects.get(nombre="item t2")
		vitem2 = VersionItem.objects.get(proxy=item2)

		newRelacionItems(fst.id,"Padre-Hijo",vitem1.id, vitem2.id)
		rt = Relacion.objects.get(antecesor=item1.id)
		self.assertEqual(rt.sucesor.id,item2.id)

		newItem("item t3",2,fst.id,ti.id,atributos)
		item3 = Item.objects.get(nombre="item t3")
		vitem3 = VersionItem.objects.get(proxy=item3)

		newRelacionItems(fst.id,"Padre-Hijo",vitem2.id, vitem3.id)
		rt = Relacion.objects.get(antecesor=item2.id)
		self.assertEqual(rt.sucesor.id,item3.id)

		try:
			newRelacionItems(fst.id,"Padre-Hijo",vitem3.id, vitem1.id)
			rt = Relacion.objects.get(antecesor=item3.id)
		except Exception, e:
			print e
