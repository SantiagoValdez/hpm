from principal.models import Usuario
from principal.models import Proyecto
from principal.models import Rol
from principal.models import Permiso
from django.contrib import admin

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Proyecto)
admin.site.register(Rol)
admin.site.register(Permiso)
