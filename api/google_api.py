#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

# Imports the Google Cloud client library
from google.cloud import speech, texttospeech, language, speech_v1p1beta1
import random
import time

__version__ = "1.30.0"

logger = logging.getLogger("speech-server")

class GoogleApi(object):

    def __init__(self, profile):
        try:
            self.profile = profile

            # Instantiates a client
            self.clientAsr = speech.SpeechClient()
            self.clientAsrBeta = speech_v1p1beta1.SpeechClient()
            self.clientTts = texttospeech.TextToSpeechClient()
            self.clientSentiment = language.LanguageServiceClient()

        except Exception as e:
            logger.error(e)


    def sendAudioFile(self, file, speakers=1, punctuation=False):
        r = ''
        try:
            config = speech.types.RecognitionConfig(
                encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                enable_automatic_punctuation=punctuation,
                language_code='pt-BR'
            )

            if (speakers > 1):
                audio = speech_v1p1beta1.types.RecognitionAudio(content=file)
                config = speech_v1p1beta1.types.RecognitionConfig(
                    encoding=speech_v1p1beta1.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code='pt-BR',
                    enable_speaker_diarization=True,
                    # enable_automatic_punctuation=punctuation,
                    diarization_speaker_count=speakers
                )
                # Detects speech in the audio file
                response = self.clientAsrBeta.recognize(config, audio)
            else:
                audio = speech.types.RecognitionAudio(content=file)
                # Detects speech in the audio file
                response = self.clientAsr.recognize(config, audio)

            if (speakers > 1):
                # The transcript within each result is separate and sequential per result.
                # However, the words list within an alternative includes all the words
                # from all the results thus far. Thus, to get all the words with speaker
                # tags, you only have to take the words list from the last result:
                result = response.results[-1]

                words_info = result.alternatives[0].words
                prev_speaker_tag = result.alternatives[0].words[0].speaker_tag

                r = "{}:".format(prev_speaker_tag)

                for i in words_info:
                    logger.debug(i)
                    print(i)
                    if (i.speaker_tag != prev_speaker_tag):
                        # print('\n')
                        # print("Speaker {} : ".format(i.speaker_tag))

                        print(r + '\n')

                        r += "\n {}:".format(i.speaker_tag)

                    r += " " + i.word

                    prev_speaker_tag = i.speaker_tag  # SPEAKER

                #print(r + '\n')

                #spk = ['', '', '', '', '']

                # Printing out the output:
                #for word_info in words_info:
                    #spk[int(word_info.speaker_tag) - 1] += u' {}'.format(word_info.word)
                    #print(word_info)


                #r += u'speakers:['
                #for x in range(0, 5):

                    #if (x > 0): r += ','
                    #r += '{"index": ' + str(x)
                    #r += ' "message": "' + spk[x].strip() + '"}'

                #r += u']'
            else:
                for result in response.results:
                    r += u'alternatives:[{"index":0, "text":"' + result.alternatives[0].transcript + '", "score":' + str(result.alternatives[0].confidence) + '}]'

            logger.debug(result)

        except Exception as e:
            logger.error(e)

        return r

    def createFileTts(self, text, voice):
        self.filename = None
        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.types.SynthesisInput(text=text)

            #gender
            gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            if (voice.lower() == "male"):
                gender = texttospeech.enums.SsmlVoiceGender.MALE
                #print(gender)

            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.types.VoiceSelectionParams(language_code='pt-BR', ssml_gender=gender)

            # Select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = self.clientTts.synthesize_speech(synthesis_input, voice, audio_config)

            self.ts = time.time()
            self.filename = '%s.wav' % (self.ts + random.random())
            self.path=self.profile.getFilePath() + self.filename

            # The response's audio_content is binary.
            with open(self.path, 'wb') as out:
                # Write the response to the output file.
                out.write(response.audio_content)

        except Exception as e:
            logger.error(e)

        return self.filename

    def analyzeSentiment(self, text):
        r = ''
        try:
            # The text to analyze
            document = language.types.Document(content=text, type=language.enums.Document.Type.PLAIN_TEXT)

            # Detects the sentiment of the text
            sentiment = self.clientSentiment.analyze_sentiment(document=document).document_sentiment

            #print('Text: {}'.format(text))
            #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

            r += u'{"sentiment":{'
            r += '"text": "' + text + '"'
            r += ', "score": "{}"'.format(sentiment.score)
            r += ', "magnitude"{}"'.format(sentiment.magnitude)
            r += '}}'

        except Exception as e:
            logger.error(e)

        return r