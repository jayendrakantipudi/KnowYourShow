from django.contrib import admin
from .models import cast,profession,director,producer

# Register your models here.

admin.site.register(cast)
admin.site.register(profession)
admin.site.register(director)
admin.site.register(producer)
