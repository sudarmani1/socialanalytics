import glob
import os
import traceback

import psycopg2
from django.conf import settings
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()

from django.contrib.auth import get_user_model

User = get_user_model()

# dbengine = settings.DATABASES['default']['ENGINE']
# dbname = settings.DATABASES['default']['NAME']
# dbhost = settings.DATABASES['default']['HOST']
# dbuser = settings.DATABASES['default']['USER']
# dbpass = settings.DATABASES['default']['PASSWORD']
# dbport = settings.DATABASES['default']['PORT']


def createDatabase():
    result = False
    try:
        dbname = settings.DATABASES['default']['NAME']
        dbhost = settings.DATABASES['default']['HOST']
        dbuser = settings.DATABASES['default']['USER']
        dbpass = settings.DATABASES['default']['PASSWORD']
        dbport = settings.DATABASES['default']['PORT']

        con = psycopg2.connect(dbname="postgres", user=dbuser, password=dbpass, host=dbhost, port=dbport)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("creating database...{0}".format(dbname))
        cursor = con.cursor()
        createsql = "create database %s " % (dbname)
        cursor.execute(createsql)
        cursor.close()
        con.close()
        print("created database...{0}".format(dbname))
        result = True
    except Exception as error:
        print(traceback.format_exc())
        raise error
    return result


def dropDatabase():
    result = False
    try:
        dbname = settings.DATABASES['default']['NAME']
        dbhost = settings.DATABASES['default']['HOST']
        dbuser = settings.DATABASES['default']['USER']
        dbpass = settings.DATABASES['default']['PASSWORD']
        dbport = settings.DATABASES['default']['PORT']

        con = psycopg2.connect(dbname="postgres", user=dbuser, password=dbpass, host=dbhost)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        dropsql = 'drop database %s' % (dbname)
        print("droping database...{0}".format(dbname))
        try:
            cursor.execute(dropsql)
        except:
            print(traceback.format_exc())
        cursor.close()
        con.close()
        print("dropped database...{0}".format(dbname))
        result = True
    except Exception as error:
        print(traceback.format_exc())
        # raise error
    return result


def CreateRootUser():
    user = User()
    user.first_name = settings.DEFAULT_USER_FIRSTNAME
    user.last_name = settings.DEFAULT_USER_LASTNAME
    user.username = settings.DEFAULT_USER_NAME
    user.set_password = settings.DEFAULT_USER_PASSWORD
    user.email = settings.DEFAULT_USER_EMAIL
    user.is_staff = settings.DEFAULT_USER_IS_STAFF
    user.is_active = settings.DEFAULT_USER_ACTIVE
    user.is_superuser = settings.DEFAULT_USER_IS_SUPERUSER
    user.save()
    print(f"User created with username:{user.username}, Password:{settings.DEFAULT_USER_PASSWORD}")


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
