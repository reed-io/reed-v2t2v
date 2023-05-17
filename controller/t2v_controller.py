import logging
import os.path
import threading
import time

import edge_tts
import pyttsx3
from fastapi import APIRouter, Form, Request
from starlette.responses import FileResponse

from define.ReedV2T2VErrorCode import ReedV2T2VErrorCode
from define.ReedResult import ReedResult

from utils.EnderUtil import StringUtil, SysUtil, TimeUtil

t2v = APIRouter()

USER_HOME = SysUtil.get_user_dir()
TTS_FILE_NAME = "reed_tts"

GENDER = {"Male", "Female"}

LOCALES = {'lv-LV', 'en-ZA', 'pt-BR', 'fr-FR', 'ne-NP', 'es-MX', 'es-UY', 'zu-ZA', 'bn-IN', 'en-US', 'ms-MY', 'gl-ES',
             'nl-NL', 'sk-SK', 'ps-AF', 'ga-IE', 'en-TZ', 'en-KE', 'vi-VN', 'nb-NO', 'en-CA', 'en-PH', 'sw-KE', 'ar-KW',
             'fr-CH', 'en-NZ', 'es-PY', 'ta-SG', 'pt-PT', 'es-BO', 'es-GQ', 'ca-ES', 'cy-GB', 'de-DE', 'el-GR', 'ko-KR',
             'lo-LA', 'en-SG', 'et-EE', 'ar-LB', 'sr-RS', 'es-NI', 'ja-JP', 'uz-UZ', 'fi-FI', 'it-IT', 'es-PR', 'ka-GE',
             'nl-BE', 'my-MM', 'es-HN', 'ta-MY', 'so-SO', 'fr-CA', 'ar-JO', 'es-US', 'bg-BG', 'kk-KZ', 'es-PE', 'sv-SE',
             'uk-UA', 'ro-RO', 'hr-HR', 'es-AR', 'fa-IR', 'bn-BD', 'da-DK', 'af-ZA', 'ar-QA', 'lt-LT', 'fr-BE', 'en-AU',
             'kn-IN', 'ar-MA', 'sq-AL', 'en-IN', 'km-KH', 'pl-PL', 'zh-CN-shaanxi', 'zh-CN', 'tr-TR', 'ar-SY', 'jv-ID',
             'cs-CZ', 'mt-MT', 'ar-SA', 'es-GT', 'ta-IN', 'id-ID', 'zh-TW', 'ur-PK', 'ur-IN', 'ml-IN', 'ar-TN',
             'fil-PH', 'zh-CN-liaoning', 'es-CO', 'bs-BA', 'es-CR', 'es-SV', 'ar-IQ', 'zh-HK', 'de-AT', 'he-IL',
             'en-HK', 'es-ES', 'su-ID', 'sw-TZ', 'de-CH', 'ar-LY', 'th-TH', 'es-DO', 'gu-IN', 'hi-IN', 'am-ET', 'en-IE',
             'ta-LK', 'az-AZ', 'ar-DZ', 'is-IS', 'es-PA', 'en-NG', 'mn-MN', 'en-GB', 'mr-IN', 'ar-AE', 'ar-OM', 'mk-MK',
             'es-VE', 'sl-SI', 'ar-YE', 'ar-EG', 'hu-HU', 'es-EC', 'si-LK', 'ar-BH', 'te-IN', 'ru-RU', 'es-CU', 'es-CL'}

LANGUAGES = {'sk', 'vi', 'nl', 'am', 'gu', 'lv', 'cy', 'zu', 'fi', 'ne', 'ta', 'th', 'en', 'kk', 'sq', 'jv', 'bg', 'lo',
             'mn', 'si', 'kn', 'hr', 'gl', 'ml', 'ka', 'ps', 'ga', 'zh', 'hu', 'ja', 'mr', 'sr', 'mk', 'uk', 'el', 'bs',
             'lt', 'mt', 'ru', 'pt', 'pl', 'es', 'cs', 'he', 'is', 'it', 'af', 'fr', 'km', 'fa', 'sl', 'id', 'ca', 'de',
             'su', 'bn', 'fil', 'uz', 'nb', 'te', 'my', 'ro', 'az', 'so', 'et', 'ko', 'ar', 'hi', 'sv', 'ms', 'ur',
             'da', 'tr', 'sw'}

@t2v.get("/languages", tags=["获取支持的语言列表"])
async def get_support_languages(cache: bool = False):
    if cache:
        result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, LANGUAGES)
        return result
    voice_manager = await edge_tts.VoicesManager.create()
    voice_list = voice_manager.find()
    language_set = set(map(lambda voice: voice["Language"], voice_list))
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, language_set)
    return result

@t2v.get("/locales", tags=["获取支持的Locale列表"])
async def get_support_locales(cache: bool = False):
    if cache:
        result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, LOCALES)
        return result
    voice_list = await edge_tts.list_voices()
    locale_set = set(map(lambda voice: voice["Locale"], voice_list))
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, locale_set)
    return result

@t2v.get("/voices", tags=["根据条件获取声音列表"])
async def get_voices(language: str = "zh", voice_gender: str = "Female"):
    if language not in LANGUAGES:
        logging.warning(f"parameter error: {language} is invalidate or not in supported list")
        result = ReedResult.get(ReedV2T2VErrorCode.LANGUAGE_INVALIDATE, language)
        return result
    if voice_gender not in GENDER:
        logging.warning(
            f"parameter error: voice_gender:{voice_gender} is invalidate, only Male or Female accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.VOICE_GENDER_INVALIDATE, voice_gender)
        return result

    voices_manager = await edge_tts.VoicesManager.create()
    voices = voices_manager.find(Gender=voice_gender, Language=language)
    voices_short_name_list = list(map(lambda voice: voice["ShortName"], voices))
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, voices_short_name_list)
    return result

@t2v.get("/voices/all", tags=["获取全部声音列表"])
async def get_voices():
    voices = await edge_tts.list_voices()
    voices_short_name_list = list(map(lambda voice: voice["ShortName"], voices))
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, voices_short_name_list)
    return result



@t2v.post(path="/", tags=["文字转语音"])
async def convert_text_to_voice_edge_tts(text: str = Form(None), speed_rate: int = Form(0), volume_rate: int = Form(0),
                                voice_name: str = Form("Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)"),
                                audio_type: str = Form("mp3")):
    if StringUtil.isEmpty(text):
        logging.warning(f"parameter error: text is empty!")
        result = ReedResult.get(ReedV2T2VErrorCode.TEXT_EMPTY, text)
        return result
    if not type(speed_rate) is int or speed_rate > 30 or speed_rate < -30:
        logging.warning(f"parameter error: speed_rate:{speed_rate} is invalidate, only integer between -30 and 30 accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.SPEED_RATE_INVALIDATE, speed_rate)
        return result
    speed_rate = ("+" if speed_rate >= 0 else "-") + str(speed_rate * 10) + "%"
    logging.debug(f"speed_rate={speed_rate}")
    if not type(volume_rate) is int or volume_rate > 30 or volume_rate < -30:
        logging.warning(f"parameter error: volume_rate:{volume_rate} is invalidate, only integer between -30 and 30 accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.VOLUME_RATE_INVALIDATE, volume_rate)
        return result
    volume_rate = ("+" if volume_rate >= 0 else "-") + str(volume_rate*10) + "%"
    logging.debug(f"volume_rate={volume_rate}")
    if StringUtil.isEmpty(voice_name):
        logging.warning(f"parameter error: voice_name is empty!")
        result = ReedResult.get(ReedV2T2VErrorCode.VOICE_NAME_EMPTY, voice_name)
        return result
    if audio_type not in ("mp3", "wav", "m4a"):
        logging.warning(f"parameter error: audio_type is invalidate! only mp3, wav, m4a accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.AUDIO_TYPE_INVALIDATE, audio_type)
        return result
    filename = TTS_FILE_NAME + "." + audio_type
    communicate = edge_tts.Communicate(text, voice_name, rate=speed_rate, volume=volume_rate)
    await communicate.save(USER_HOME + SysUtil.file_separator() + filename)
    return FileResponse(filename=filename, path=USER_HOME + SysUtil.file_separator() + filename)


@t2v.post(path="/v2", tags=["文字转语音"])
def convert_text_to_voice_pyttsx3(text: str = Form(None), speed_rate: int = Form(0), volume_rate: int = Form(0),
                                audio_type: str = Form("mp3")):
    if StringUtil.isEmpty(text):
        logging.warning(f"parameter error: text is empty!")
        result = ReedResult.get(ReedV2T2VErrorCode.TEXT_EMPTY, text)
        return result
    if not type(speed_rate) is int or speed_rate > 200 or speed_rate <= -200:
        logging.warning(f"parameter error: speed_rate:{speed_rate} is invalidate, only integer between -200 and 200 accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.SPEED_RATE_INVALIDATE_PYTTSX3, speed_rate)
        return result
    speed_rate = 200 + speed_rate if speed_rate >= 0 else 200 - speed_rate
    logging.debug(f"speed_rate={speed_rate}")
    if not type(volume_rate) is int or volume_rate > 50 or volume_rate <= -50:
        logging.warning(f"parameter error: volume_rate:{volume_rate} is invalidate, only integer between -50 and 50 accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.VOLUME_RATE_INVALIDATE_PYTTSX3, volume_rate)
        return result
    volume_rate = 1.0 + volume_rate/10 if volume_rate >= 0 else 1.0 - volume_rate/10
    logging.debug(f"volume_rate={volume_rate}")
    if audio_type not in ("mp3", "wav", "m4a"):
        logging.warning(f"parameter error: audio_type is invalidate! only mp3, wav, m4a accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.AUDIO_TYPE_INVALIDATE, audio_type)
        return result
    filename = TTS_FILE_NAME + "." + audio_type
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', "zh")
    t1 = TimeUtil.unix_now()
    file_path = USER_HOME + SysUtil.file_separator() + filename
    if os.path.exists(file_path):
        os.remove(file_path)
    engine.save_to_file(text=text, filename=file_path)
    t2 = TimeUtil.unix_now()
    logging.debug(f"t2v cost: {t2 - t1} ms")
    engine.runAndWait()
    engine.stop()
    while not os.path.exists(file_path):  # 临时方案
        logging.debug("file not ready")
        time.sleep(0.1)
    return FileResponse(filename=filename, path=file_path)
