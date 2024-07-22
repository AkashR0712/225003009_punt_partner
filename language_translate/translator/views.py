from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator  
import os
import base64
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import io
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import pyttsx3
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

@csrf_exempt
def translate_speech(request):
    if request.method == 'POST':
        try:
            audio_file = request.FILES.get('audio')
            target_language = request.POST.get('target_language', 'en')
            if not audio_file or not target_language:
                logger.error("Missing required parameters: audio file or target language")
                return JsonResponse({'error': 'Missing required parameters'}, status=400)
            file_extension = os.path.splitext(audio_file.name)[1].lower()

            if file_extension != '.wav':
                logger.error("Unsupported file format. Only WAV files are supported.")
                return JsonResponse({'error': 'Unsupported file format'}, status=400)
            
            wav_path = os.path.join('/tmp', 'uploaded_audio.wav')
            with open(wav_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)

            try:
                detected_text = recognizer.recognize_google(audio_data)
                logger.info(f"Detected text: {detected_text}")
            except sr.UnknownValueError:
                logger.error("Google Web Speech API could not understand the audio")
                return JsonResponse({'error': 'Could not understand the audio'}, status=400)
            except sr.RequestError:
                logger.error("Could not request results from Google Web Speech API")
                return JsonResponse({'error': 'Error requesting results from Google Web Speech API'}, status=500)

            try:
                translator = Translator()
                translated_text = translator.translate(detected_text, dest=target_language).text
                logger.info(f"Translated text: {translated_text}")
            except Exception as e:
                logger.error(f"Error translating text: {e}")
                return JsonResponse({'error': 'Error translating text'}, status=500)

            try:
                tts = gTTS(text=translated_text, lang=target_language)
                tts_output = io.BytesIO()
                tts.save(tts_output)
                tts_output.seek(0)

                audio_base64 = base64.b64encode(tts_output.read()).decode('utf-8')
            except Exception as e:
                logger.error(f"Error generating speech: {e}")
                return JsonResponse({'error': 'Error generating speech'}, status=500)

            return JsonResponse({'translated_text': translated_text, 'audio_content': audio_base64})

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return JsonResponse({'error': 'Error processing audio'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)