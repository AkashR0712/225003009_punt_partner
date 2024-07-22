# 225003009_punt_partner 
# Language Translation Application

This Django application provides functionality for translating text and speech between different languages. 

## Setup

### 1. Install Django Framework

Ensure you have Python 3.8 or higher installed. You can install Django using pip:

```bash
pip install django
git clone https://github.com/AkashR0712/225003009_punt_partner.git
cd language_translator
pip install -r requirements.txt 
python manage.py migrate
python manage.py runserver
 
## Usage

### Text Translation

1. Enter text in the text field.
2. Choose the target language from the dropdown menu.
3. Click the "Translate Text" button.

### Speech Translation

1. Ensure your audio file is in `.wav` format. If not, use an online converter to convert it to `.wav`.
2. Upload the `.wav` audio file.
3. Choose the target language from the dropdown menu.
4. Click the "Translate Speech" button.
5. After translation, you can listen to the translated text by clicking the "Play Translated Text" button.

## Notes

- Only `.wav` audio files are supported for speech translation.
- Ensure you have the correct format for both text and audio translations.
