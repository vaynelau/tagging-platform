# login/admin.py

from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Admin)
admin.site.register(models.Task)
