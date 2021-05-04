# Register your models here.
from django.contrib import admin
from django.apps import apps

# Register your models here.

my_app = apps.get_app_config('insta')

for model in list(my_app.get_models()):
    admin.site.register(model)
