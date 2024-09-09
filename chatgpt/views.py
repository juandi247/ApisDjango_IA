from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR
# Create your views here.
from dotenv import load_dotenv
import os

load_dotenv()
#PRUEBAS PARA FLASHCARDS

from groq import Groq

client = Groq(
    api_key=os.getenv('grok_api_key')
)

@api_view(['POST'])
def askGroqDeck(request):

    nivel=request.data.get('nivel', '')
    num_palabras=request.data.get('number','')
    tema=request.data.get('tema','')
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""Creame una lista de flashcards de {num_palabras} palabras,con solo palabra en aleman y frente la de español de tema "{tema}" con un nivel de aleman que le resulte dificiles a las personas de nivel: {nivel}, 
            sin ningun texto extra y que solo sean las palabras y que esten ordenadas de forma que queden (palabra alemana:palabraespañol , (segundapalabraalemana:español, y asi))
            por ultimo, quiero que el texto que me des no tenga nada de texto extra, es decir solo quiero que sean las palabras y ya""",
        }
    ],
    model="llama-3.1-70b-versatile",
    )
    
    respuesta=chat_completion.choices[0].message.content
    flashcards = {}
    for line in respuesta.strip().split('\n'):
        if ':' in line:
            german_word, spanish_word = line.split(':', 1)
            flashcards[german_word.strip()] = spanish_word.strip()

    return Response(flashcards,status=HTTP_200_OK)
                






    #CORRECION DE FRASE

@api_view(['POST'])
def CorreccionFrase(request):

    Palabra=request.data.get('palabra', '')
    Frase=request.data.get('frase','')
   
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""Corrigeme la siguiente frase en aleman : {Frase} que contiene la palabra {Palabra}. Si la frase es correcta solo dime Correcto! pero si es incorrecta dime una 
            correccion pequeña de la frase. Sin la traduccion de la frase. Con la siguiente estructura= si contesto la frase bien escribe ->Correcto , si contesto la frase mal escribe. La frase Correcta es->>: frase correcta""",
        }
    ],
    model="llama-3.1-70b-versatile",
    )
    
    respuesta=chat_completion.choices[0].message.content
    flashcards = {}
    for line in respuesta.strip().split('\n'):
        if ':' in line:
            german_word, spanish_word = line.split(':', 1)
            flashcards[german_word.strip()] = spanish_word.strip()

    return Response(flashcards,status=HTTP_200_OK)
                










#PRUEBA OPEN AI





#PRUEBA AZURE PARA ESCUCHAR LAS PALABRAS

import azure.cognitiveservices.speech as speech

api_key=os.getenv('azure_api_key')
region=os.getenv('region_azure')

#uguauu
@api_view(['POST'])
def listen(request):
    Palabra = request.data.get('palabra', '')

    speech_conf = speech.SpeechConfig(subscription=api_key, region=region)
    speech_conf.speech_synthesis_voice_name = 'de-DE-ChristophNeural' 

    audio_conf = speech.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speech.SpeechSynthesizer(speech_config=speech_conf, audio_config=audio_conf)
    
    result = speech_synthesizer.speak_text(Palabra)    

    if result.reason == speech.ResultReason.SynthesizingAudioCompleted:
        return Response({"message": "Speech synthesis completed."}, status=HTTP_200_OK)
    else:
        # Imprimir detalles del error
        cancellation_details = result.cancellation_details
        error_message = f"Speech synthesis failed: {result.reason}"
        if cancellation_details.reason == speech.CancellationReason.Error:
            error_message += f" Error details: {cancellation_details.error_details}"

        return Response({"error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)







