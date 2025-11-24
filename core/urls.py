"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication


schema_view = get_schema_view(
    openapi.Info(
        title="Maisha Uni API",
        default_version='v1',
        description="""
        Maisha Uni Student Success Platform API Documentation.

        This API powers the Maisha Uni platform, enabling students and institutions to:
        - Manage user accounts and profiles
        - Post and view announcements
        - Discover opportunities (internships, jobs, scholarships)
        - And much more...
        
        ## Authentication
        This API uses JWT authentication. To authenticate your requests:
        1. Use the `/api/auth/login/` endpoint to get your access token
        2. Include the token in the Authorization header: `Bearer <your_token>`
        
        ## User Roles
        - **Students**: Can view announcements and opportunities, manage their profile
        - **Admins**: Can create announcements and opportunities, manage content
        """,
        terms_of_service="https://www.maishauni.com/terms/",
        contact=openapi.Contact(email="support@maishauni.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/opportunities/', include('opportunities.urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Root path redirect to Swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),
]
