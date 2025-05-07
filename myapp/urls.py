from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'submissions', views.StudentSubmissionViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/submit-form/', views.submit_form, name='submit-form'),
    path('api/export-data/', views.export_data, name='export-data'),
]