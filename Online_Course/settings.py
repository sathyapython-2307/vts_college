import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Make sure this is included
    'core',  # Your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Online_Course.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# First check if razorpay is available
try:
    import razorpay  # noqa: F401
    RAZORPAY_PACKAGE_AVAILABLE = True
except ImportError:
    print('Warning: razorpay package not installed. Install it with: pip install razorpay')
    RAZORPAY_PACKAGE_AVAILABLE = False

# Razorpay Test Credentials (for development environment only)
RAZORPAY_SETTINGS = {
    'ENABLED': True,  # Enable Razorpay gateway
    'KEY_ID': 'rzp_test_RYnB6bkmpifFj4',  # Test mode API key
    'KEY_SECRET': '4oKd2Eg9xRHnzsSK7IzD2xKD',  # Test mode API secret
    'CURRENCY': 'INR'  # Default currency
}

# For production, use environment variables or a secure configuration file
if not DEBUG:
    from django.core.exceptions import ImproperlyConfigured
    try:
        RAZORPAY_SETTINGS.update({
            'ENABLED': os.environ.get('RAZORPAY_ENABLED', 'true').lower() == 'true',
            'KEY_ID': os.environ['RAZORPAY_KEY_ID'],
            'KEY_SECRET': os.environ['RAZORPAY_KEY_SECRET'],
            'CURRENCY': os.environ.get('RAZORPAY_CURRENCY', 'INR')
        })
    except KeyError as e:
        raise ImproperlyConfigured(f'Missing required environment variable: {e}')

# Direct settings for easier access in views
RAZORPAY_ENABLED = RAZORPAY_PACKAGE_AVAILABLE and RAZORPAY_SETTINGS['ENABLED']
RAZORPAY_KEY_ID = RAZORPAY_SETTINGS['KEY_ID']
RAZORPAY_KEY_SECRET = RAZORPAY_SETTINGS['KEY_SECRET']
RAZORPAY_CURRENCY = RAZORPAY_SETTINGS['CURRENCY']

# Print configuration state during startup (with security in mind)
print('DEBUG: RAZORPAY CONFIG:', {
    'PACKAGE_AVAILABLE': RAZORPAY_PACKAGE_AVAILABLE,
    'SETTINGS_ENABLED': RAZORPAY_SETTINGS['ENABLED'],
    'ENABLED': RAZORPAY_ENABLED,
    'KEY_ID': RAZORPAY_KEY_ID,
    'KEY_SECRET_LENGTH': len(RAZORPAY_KEY_SECRET) if RAZORPAY_KEY_SECRET else 0,
    'CURRENCY': RAZORPAY_CURRENCY,
    'MODE': 'TEST' if DEBUG else 'PRODUCTION'
})