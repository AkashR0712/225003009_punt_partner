from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator 
import os
import base64
import logging
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator
import pyttsx3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import pyttsx3
import base64
logger = logging.getLogger(__name__)
def index(request):
    return render(request, 'index.html')

def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        target_language = request.POST.get('target_language')

        translator = Translator()
        detected_language = translator.detect(text).lang
        result = translator.translate(text, src=detected_language, dest=target_language)

        return JsonResponse({'detected_language': detected_language, 'translated_text': result.text})

import os
import base64
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment
import speech_recognition as sr
from googletrans import Translator
import pyttsx3

logger = logging.getLogger(__name__)

@csrf_exempt
def translate_speech(request):
    if request.method == 'POST':
        try:
            # Get the uploaded audio file and target language
            audio_file = request.FILES.get('audio')
            target_language = request.POST.get('target_language', 'en')

            if not audio_file or not target_language:
                logger.error("Missing required parameters: audio file or target language")
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            # Convert MP3 to WAV using pydub
            audio = AudioSegment.from_file(audio_file, format="mp3")
            wav_path = os.path.join('/tmp', 'temp_audio.wav')
            audio.export(wav_path, format='wav')

            # Initialize Speech Recognizer
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)

            # Recognize speech using Google Web Speech API
            detected_text = recognizer.recognize_google(audio_data)
            logger.info(f"Detected text: {detected_text}")

            # Translate the detected text
            translator = Translator()
            translated_text = translator.translate(detected_text, dest=target_language).text
            logger.info(f"Translated text: {translated_text}")

            # Generate speech from the translated text
            tts_engine = pyttsx3.init()
            tts_output_path = os.path.join('/tmp', 'translated_speech.mp3')
            tts_engine.save_to_file(translated_text, tts_output_path)
            tts_engine.runAndWait()

            # Convert generated audio to base64
            with open(tts_output_path, 'rb') as audio_out:
                audio_base64 = base64.b64encode(audio_out.read()).decode('utf-8')

            return JsonResponse({'translated_text': translated_text, 'audio_content': audio_base64})

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return JsonResponse({'error': 'Error processing audio'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)