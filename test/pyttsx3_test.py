import time

import pyttsx3
from utils.EnderUtil import TimeUtil

engine = pyttsx3.init()
engine.setProperty('rate', 90)
engine.setProperty('volume', 1.0)
# voice = engine.getProperty('voices')
# for v in voice:
#     print(v)
# print(voice[0])
# engine.setProperty('voice', voice[0].id)
engine.setProperty('voice', "zh")
engine.say("hello world!")
engine.say("你好，哈哈哈哈哈")
t1 = TimeUtil.unix_now()
# engine.save_to_file(text="测试一下 pyttsx3 没毛病！", filename="D:\\pyttsx3_test.m4a")
t2 = TimeUtil.unix_now()
print(t2-t1)
engine.runAndWait()
engine.stop()