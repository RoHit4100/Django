from decouple import config

# Database settings
DB_ENGINE = config('DB_ENGINE', default='django.db.backends.postgresql')
DB_NAME = config('DB_NAME', default='LearningService')
DB_USER = config('DB_USER', default='postgres')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default=5432, cast=int)

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

