from gtts import gTTS # 인공지능이 들을 수 있게 해주는 터미널 (pip install gTTs) 
from playsound import playsound # 인공지능이 들을 수 있게 해주는 터미널 (pip install playsound==1.2.2, 이걸로 안 하면 렉 걸림)
import time, os
import speech_recognition as sr # 인공지능이 들을 수 있게 해주는 터미널 (pip install SpeechRecognition, pip install PyAudio)

# 머신러닝 모델로 대화하는 메소드 exe파일로 만들면 오류가 있어서 놔둠
import streamlit as st # 대화 CSV 인코딩을 위해 있는 터미널그대로 넣어서 pip 하면 됨
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

@st.cache(allow_output_mutation=True)
def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

@st.cache(allow_output_mutation=True)
def get_dataset():
    df = pd.read_csv(
        'password1.csv', encoding='cp949')
    df['embedding'] = df['embedding'].apply(json.loads)
    return df

AI_clear = 1

def main_clear(filename):

    #음성 인식(듣기, STT)
    def listen(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio, language='ko')
            answer(text)

        except sr.UnknownValueError:
            print('인식 실패') #음성 인식 실패

        except sr.RequestError as e:
            print('요청 실패 : {0}',format(e)) #API KEY 오류, 네트워크 단절.

    def answer(input_text):

        model = cached_model()
        df = get_dataset()
        
        global AI_clear

        if "돌아가" in input_text or '모르겠어' in input_text or '몰라' in input_text:

            speak("다시 메인으로 돌아가겠습니다.")

            stop_listening_clear(wait_for_stop=False) # 더 이상 안 듣기.

            # while 문에 break를 걸기 위해 있는 변수
            
            AI_clear = 3


        embedding = model.encode(input_text)

        # 암호와 대화가 있는 곳
        df['distance'] = df['embedding'].map(
            lambda x: cosine_similarity([embedding], [x]).squeeze())

        answer = df.loc[df['distance'].idxmax()]


        if  filename in str(answer['파일']):

            speak("암호를 확인했습니다.")

            df2 = df[df.파일 != filename]

            df2.to_csv('password.csv', index=False)

            stop_listening_clear(wait_for_stop=False) # 더 이상 안 듣기.

            # while 문에 break를 걸기 위해 있는 변수
            AI_clear = 5 

        else :
            speak("암호가 틀립니다.")
            speak("다시 한번 말씀해주세요.")

    #인공지능 대답 (TTS)
    def speak(text):
        base_voice = 'voice.mp3'
        tts = gTTS(text=text, lang ='ko')
        tts.save(base_voice)
        playsound(base_voice)
        if os.path.exists(base_voice): #vioce 기존에 있던 파일 삭제
            os.remove(base_voice)

    #마이크로 듣고 인풋되는 부분.
    r = sr.Recognizer()
    m = sr.Microphone()

    stop_listening_clear = r.listen_in_background(m, listen) 

    speak("암호를 말씀해주세요.")

    while True:
        if AI_clear == 5 or AI_clear == 3:
            break
        else:
            time.sleep(0.05)