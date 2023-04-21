from define.BaseErrorCode import BaseErrorCode
from define.ErrorCode import ErrorCode

class ReedV2T2VErrorCode(BaseErrorCode):
    """
        0x00E0~0x00FF
    """
    LANGUAGE_INVALIDATE = ErrorCode(code=0x00e0, message="language is invalidate or not in supported list")
    VOICE_GENDER_INVALIDATE = ErrorCode(code=0x00e1, message="voice_gender is invalidate, only Male or Female accepted!")
    TEXT_EMPTY = ErrorCode(code=0x00e2, message="text is empty!")
    SPEED_RATE_INVALIDATE = ErrorCode(code=0x00e3, message="speed_rate is invalidate, only integer between -30 and 30 accepted!")
    VOLUME_RATE_INVALIDATE = ErrorCode(code=0x00e4, message="volume_rate is invalidate, only integer between -30 and 30 accepted!")
    VOICE_NAME_EMPTY = ErrorCode(code=0x00e5, message="voice_name is empty!")
    AUDIO_TYPE_INVALIDATE = ErrorCode(code=0x00e6, message="audio_type is invalidate! only mp3, wav, m4a accepted!")
    SPEED_RATE_INVALIDATE_PYTTSX3 = ErrorCode(code=0x00e7, message="speed_rate is invalidate, only integer between -200 and 200 accepted!")
    VOLUME_RATE_INVALIDATE_PYTTSX3 = ErrorCode(code=0x00e8, message="volume_rate is invalidate, only integer between -50 and 50 accepted!")
    AUDIO_FILE_INVALIDATE = ErrorCode(code=0x00e9, message="upload file is not a validate audio, only m4a or mp3 or wav accepted!")