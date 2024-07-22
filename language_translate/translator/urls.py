from django.urls import path
from .views import index, translate_text, translate_speech

urlpatterns = [
    path('', index, name='index'), 
    path('translate-text/', translate_text, name='translate_text'), 
    path('translate-speech/', translate_speech, name='translate_speech'),  
]
