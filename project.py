from gtts import gTTS # 인공지능이 들을 수 있게 해주는 터미널 (pip install gtts) 
from playsound import playsound # 인공지능이 들을 수 있게 해주는 터미널 (pip install playsound==1.2.2, 이걸로 안 하면 렉 걸림)
import time, os
import speech_recognition as sr # 인공지능이 들을 수 있게 해주는 터미널 (pip install SpeechRecognition, pip install PyAudio)
import project_lock
import project_clear
import socket

AI = 1

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

    if '암호화' in input_text:

        count = 0

        file = input_text

        file = file.replace("암호화","")
        file = file.replace("파일","")
        file = file.replace("해", "")
        file = file.replace("의", "")
        file = file.replace("줘", "")
        file = file.replace("file", "")
        file = file.replace(" ", "")

        speak(file + "파일을 찾고 있습니다.")

        #파일 찾는 함수
        def find_file(basedir, filename):
            for dirname, dirs, files in os.walk(basedir):
                if filename in files:
                    yield os.path.join(dirname, filename)

        # 파일 찾아서 자바와 연동 된 텍스트 파일에 쓰기
        for found in find_file ('C:/Test', file + '.txt'):

            count = 1

        if count == 0:

            speak("파일을 찾을 수 없습니다.")

            speak("다시 한 번 말씀해주세요.")

        if count == 1:
            
            
            speak(file + "파일의 암호화를 시작하겠습니다.")

            project_lock.main_lock(file)

            speak("완료했습니다.")
          
    elif '복호화' in input_text:

        project_clear.AI_clear = 1
        
        count = 0

        file = input_text

        file = file.replace("복호화","")
        file = file.replace("파일","")
        file = file.replace("해", "")
        file = file.replace("의", "")
        file = file.replace("줘", "")
        file = file.replace("해제", "")
        file = file.replace("제", "")
        file = file.replace("file", "")
        file = file.replace(" ", "")

        speak(file + "파일을 찾고 있습니다.")

        #파일 찾는 함수
        def find_file(basedir, filename):
            for dirname, dirs, files in os.walk(basedir):
                if filename in files:
                    yield os.path.join(dirname, filename)


        # 파일 찾아서 자바와 연동 된 텍스트 파일에 쓰기
        for found in find_file ('C:/Test', file + '.txt'):

            count = 1

        if count == 0:

            speak("파일을 찾을 수 없습니다.")

            speak("다시 한 번 말씀해주세요.")

        if count == 1:
            
            speak(file + "파일의 복호화를 시작하겠습니다.")
            
            project_clear.main_clear(file)

            if project_clear.AI_clear == 5:
                speak("완료했습니다.")

            if project_clear.AI_clear == 3:
                speak("암호를 다시 생각해주세요.")
            
            
        
    elif '종료' in input_text:

        stop_listening(wait_for_stop=False) # 더 이상 안 듣기.
        speak('종료 하겠습니다.')

        # while 문에 break를 걸기 위해 있는 변수
        global AI
        AI = 5 

    else :
        speak("다시 한 번 말씀해주세요.")


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

speak("안녕하세요.")

speak("인공지능 암호화 프로그램 입니다.")

stop_listening = r.listen_in_background(m, listen) 

while True:
    if AI == 5:
        break
    else:
        time.sleep(0.05)