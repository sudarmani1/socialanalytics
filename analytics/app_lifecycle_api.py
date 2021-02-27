import glob
import json
import os
import shutil
import sys
import traceback

import psycopg2
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()
import settings
from django.contrib.auth import get_user_model

User = get_user_model()

dbengine = "django.db.backends.postgresql_psycopg2"
dbname = settings.DATABASES['default']['NAME']
dbhost = "localhost"
dbuser = "postgres"
dbpass = "secret"
dbport = ""


def createDatabase():
    result = False
    try:
        con = psycopg2.connect(dbname="postgres", user=dbuser, password=dbpass, host=dbhost, port=dbport)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        createsql = "create database %s " % (dbname)
        cursor.execute(createsql)
        cursor.close()
        con.close()
        result = True
        print(f"Created new database {dbname}")
    except Exception as error:
        raise error
    return result


def dropDatabase():
    result = False
    try:
        con = psycopg2.connect(dbname="postgres", user=dbuser, password=dbpass, host=dbhost)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        dropsql = 'drop database %s' % (dbname)
        try:
            cursor.execute(dropsql)
        except:
            pass
        cursor.close()
        con.close()
        result = True
        print(f"DB Dropped {dbname}")
    except Exception as error:
        print(error)
        # raise error
    return result

def CreateRootUser():
        user = User()
        user.username = "admin"
        user.first_name = "admin"
        user.last_name = "test"
        user.set_password("pass4321")
        user.email = "admin@admin.com"
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        print(f"New Admin created. {user.username}")


def runMigrations():
    result = False
    try:
        # remove migration files
        app_list = [app for app in settings.INSTALLED_APPS]
        for apps in app_list:
            apps = apps.replace(".", "/")
            migration_path = os.path.join(settings.BASE_DIR, '%s/migrations' % (apps))
            for file in glob.glob(migration_path + "/0*.py"):
                os.remove(file)

        all_app_list = [app for app in settings.INSTALLED_APPS]
        for apps in all_app_list:
            if apps.startswith("SAF") or apps.startswith("SAS"):
                apps = apps.rsplit(".", 1)
                try:
                    call_command('makemigrations', '--pythonpath', apps[0].replace(".", "/"), apps[1],
                                 interactive=False)
                except Exception as e:
                    print(e)

        result = True
    except Exception as e:
        print(e)

    call_command('makemigrations', interactive=False)
    call_command('migrate', interactive=False)

    return result
