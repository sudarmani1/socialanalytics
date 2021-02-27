import os
import sys
from django.core.wsgi import get_wsgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()

import app_lifecycle_api


def init(db_init=True):
    if db_init:
        app_lifecycle_api.dropDatabase()
        app_lifecycle_api.createDatabase()
        app_lifecycle_api.runMigrations()
    # app_lifecycle_api.CreateRootUser()


if __name__ == '__main__':
    POSSIBLE_COMMANDS_LIST = ["init"]
    if len(sys.argv) < 2:
        sys.exit("""Must provide args like \n\t %s""" %
                 ("\n\t ".join(POSSIBLE_COMMANDS_LIST)))
    else:
        if sys.argv[1] in POSSIBLE_COMMANDS_LIST:
            if sys.argv[1] == 'init':
                password = input("Enter password: ")
                if password == "pass4321":
                    init()
                else:
                    print('na na na ... abort abort abort')
            else:
                print('na na na ... abort abort abort')

        else:
            sys.exit("""Invalid argument, Must provide args like \n\t %s""" %
                     ("\n\t ".join(POSSIBLE_COMMANDS_LIST)))
