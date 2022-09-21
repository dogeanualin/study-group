import site
from django.contrib import admin

from .models import Room,Topyc,Messages,User
# Register your models here.


admin.site.register(User)
admin.site.register(Topyc)
admin.site.register(Room)

admin.site.register(Messages)