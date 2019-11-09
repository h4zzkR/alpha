DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'a0310391_concat_db',
        'USER': 'a0310391_concat_db',
        'PASSWORD': '2b8wWCkg',
        'HOST': 'kupipalantin.ru',
        'OPTIONS': {
           'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
           'charset': 'utf8mb4',
        },

    }
}
DEBUG = False
