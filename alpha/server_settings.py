# TODO: Edit Database Credentials on Server
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'concat',
            'USER': 'concat',
            'PASSWORD': 's1XTPKlOjWo4',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
                'charset': 'utf8mb4',
            },

        }
    }
DEBUG = True
