import speech_recognition as sr

def wav2txt(wavfilepath):
    r = sr.Recognizer()
    sudio = ""
    with sr.AudioFile(wavfilepath) as src:
        sudio = r.record(src)
    print(r.recognize_sphinx(sudio, language="zh-CN"))


wav2txt("C:\\Users\\Ender\\Desktop\\测试.wav")
