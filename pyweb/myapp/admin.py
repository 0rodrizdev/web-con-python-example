from django.contrib import admin
from .models import (
    YourModel1,   # Cambia YourModel1 por el nombre de tu primer modelo
    YourModel2,   # Cambia YourModel2 por el nombre de tu segundo modelo
    YourModel3,   # Cambia YourModel3 por el nombre de tu tercer modelo
)

# Configuración personalizada para YourModel1
class YourModel1Admin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')  # Cambia 'field1', 'field2', 'field3' por los nombres de tus campos
    list_filter = ('field1',)  # Cambia 'field1' por el campo que deseas filtrar
    search_fields = ('field2', 'field3')  # Cambia 'field2', 'field3' por los campos que deseas buscar
    ordering = ('field1',)  # Cambia 'field1' por el campo por el cual deseas ordenar
    prepopulated_fields = {'slug': ('field1',)}  # Cambia 'slug' y 'field1' según sea necesario

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si estamos editando un objeto existente
            return ['field2', 'field3']  # Cambia por los campos que desees que sean solo de lectura
        return super().get_readonly_fields(request, obj)

# Configuración personalizada para YourModel2
class YourModel2Admin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'created_at')  # Cambia 'created_at' por el nombre de tu campo de fecha
    list_filter = ('status',)  # Cambia 'status' por el campo que deseas filtrar
    search_fields = ('field1', 'field2')
    date_hierarchy = 'created_at'  # Cambia por el campo de fecha para la jerarquía
    ordering = ('-created_at',)  # Ordenar por fecha de creación de manera descendente

# Configuración personalizada para YourModel3
class YourModel3Admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')  # Cambia 'is_active' por un campo booleano
    list_filter = ('is_active',)  # Filtro para el campo booleano
    search_fields = ('name',)
    ordering = ('name',)

    def has_delete_permission(self, request, obj=None):
        return False  # Deshabilitar eliminación de objetos para este modelo

# Registro de los modelos en el panel de administración
admin.site.register(YourModel1, YourModel1Admin)
admin.site.register(YourModel2, YourModel2Admin)
admin.site.register(YourModel3, YourModel3Admin)
# admin.site.register(ChatRoom)
#admin.site.register(ChatMessage)
#admin.site.register(UserProfile)
#admin.site.register(MessageReaction)
#admin.site.register(PrivateMessage)
#admin.site.register(Group) 
# Personalización adicional del sitio de administración
admin.site.site_header = "Mi Sitio de Administración"  # Cambia esto por el nombre de tu proyecto
admin.site.site_title = "Admin Panel"  # Título en la pestaña del navegador
admin.site.index_title = "Bienvenido al panel de administración"  # Título en la página de inicio del admin

# Puedes agregar más modelos y sus administraciones personalizadas de la misma manera
