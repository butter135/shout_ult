import speech_recognition as sr
import pyautogui
import re
import json
import asyncio

print("ウェイクワード設定 (始めの1単語が良い)")
wakeword = input()
r = sr.Recognizer()
r.pause_threshold = 0.5
r.energy_threshold = 5000
mic = sr.Microphone()
pattern = re.compile(r".*" + wakeword + ".*")

async def detect(audio):
    try:
        text = json.loads(r.recognize_vosk(audio, language='ja-JP'))["text"]
        if pattern.match(text):
            pyautogui.write("p")
        print(text)

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        return 
    except sr.RequestError as e:
        return
    
while True:
    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source, phrase_time_limit=1)
    asyncio.run(detect(audio))

