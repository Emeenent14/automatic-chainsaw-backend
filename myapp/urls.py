from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'submissions', views.StudentSubmissionViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/submit-form/', csrf_exempt(views.submit_form), name='submit_form'),
    path('api/export-data/', views.export_data, name='export-data'),
]