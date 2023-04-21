import edge_tts
import random
import asyncio
import locale

async def test():
    # voice_list = await edge_tts.list_voices()
    # for v in voice_list:
    #     print(v)

    text = "测试  测试  测试， 哈哈哈哈哈"

    voices = await edge_tts.VoicesManager.create()
    voice = voices.find(Gender="Female", Language="zh")

    communicate = edge_tts.Communicate(text, random.choice(voice)["Name"], rate="+200%", volume="+30%")
    # communicate = edge_tts.Communicate(text, "test h", rate="+200%", volume="+30%")
    await communicate.save("D:\\edge_tts_test.mp3")


async def get_locale_list():
    voice_list = await edge_tts.list_voices()
    locale_list = set(map(lambda voice: voice["Locale"], voice_list))
    print(locale_list)
    for item in locale_list:
        print(item)

async def get_language_list():
    voice_manager = await edge_tts.VoicesManager.create()
    voice_list = voice_manager.find()
    language_list = set(map(lambda voice: voice['Language'], voice_list))
    print(language_list)
    for item in language_list:
        print(item)

if __name__ == "__main__":
    # asyncio.run(test())
    asyncio.run(get_language_list())
