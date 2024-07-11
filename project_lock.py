from gtts import gTTS # 인공지능이 들을 수 있게 해주는 터미널 (pip install gTTs) 
from playsound import playsound # 인공지능이 들을 수 있게 해주는 터미널 (pip install playsound==1.2.2, 이걸로 안 하면 렉 걸림)
import time, os
import speech_recognition as sr # 인공지능이 들을 수 있게 해주는 터미널 (pip install SpeechRecognition, pip install PyAudio)
import csv
from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer

AI_lock = 1

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

def main_lock(filename):

    def listen(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio, language='ko')
            answer(text)

        except sr.UnknownValueError:
            print('인식 실패') #음성 인식 실패

        except sr.RequestError as e:
            print('요청 실패 : {0}',format(e)) #API KEY 오류, 네트워크 단절.

    def answer(input_text):

        file = input_text

        file = file.replace("로", "")
        file = file.replace("으로", "")
        file = file.replace("해", "")
        file = file.replace("줘", "")
        file = file.replace(" ", "")
        
        speak(file + "로 설정하겠습니다.")

        f = open('password1.csv', 'a', newline='', encoding='cp949')

        wr = csv.writer(f)

        wr.writerow([filename, file, file, list(model.encode(file))])

        f.close()

        stop_listening_lock(wait_for_stop=False)

        global AI_lock 
        AI_lock = 5 

    def speak(text):
        base_voice = 'voice.mp3'
        tts = gTTS(text=text, lang ='ko')
        tts.save(base_voice)
        playsound(base_voice)
        if os.path.exists(base_voice): #vioce 기존에 있던 파일 삭제
            os.remove(base_voice)

    r = sr.Recognizer()
    m = sr.Microphone()

    stop_listening_lock = r.listen_in_background(m, listen) 

    speak("비밀번호는 무엇으로 하시겠습니까?")

    while True:
        if AI_lock == 5:
            break
        else:
            time.sleep(0.05)