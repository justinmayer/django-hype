SECRET_KEY = "hunter2"
DEBUG = True
SITE_ID = 1
USE_TZ = True

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": ":memory:",
	},
}

INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django_reflinks",
]

TEMPLATES = [{
	"BACKEND": "django.template.backends.django.DjangoTemplates",
	"DIRS": [],
	"APP_DIRS": True,
	"OPTIONS": {
		"context_processors": [
			"django.template.context_processors.debug",
			"django.template.context_processors.request",
			"django.contrib.auth.context_processors.auth",
			"django.contrib.messages.context_processors.messages",
		],
	},
}]

MIDDLEWARE = [
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "tests.urls"
