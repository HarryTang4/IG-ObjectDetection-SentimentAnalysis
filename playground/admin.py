from django.contrib import admin
from .models import Photos
from .models import Login
from .models import Register
from .models import User
# Register your models here.

admin.site.register(Photos)
admin.site.register(Login)
admin.site.register(Register)
admin.site.register(User)
