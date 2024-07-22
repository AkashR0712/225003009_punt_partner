from django.urls import path
from .views import index, translate_text, translate_speech

urlpatterns = [
    path('', index, name='index'),  # Home page for the application
    path('translate-text/', translate_text, name='translate_text'),  # URL for text translation
    path('translate-speech/', translate_speech, name='translate_speech'),  # URL for speech translation
]
