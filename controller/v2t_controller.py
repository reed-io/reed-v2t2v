import logging

import torch.cuda
import whisper
from fastapi import APIRouter, Form, Request, UploadFile, File
from starlette.responses import FileResponse

from define.ReedV2T2VErrorCode import ReedV2T2VErrorCode
from define.ReedResult import ReedResult
from define.AudioFile import AudioFile

from utils.EnderUtil import StringUtil, SysUtil, FileUtil, TimeUtil

import ffmpeg
import numpy as np

v2t = APIRouter()

USER_HOME = SysUtil.get_user_dir()
TTS_FILE_NAME = "reed_tts"
CHINESE_PROMPT = "这是个案例，请按照我的想法完成转译"
MODEL_HOME = USER_HOME + SysUtil.file_separator() + ".cache/v2t2v"
GPU_SPEED_UP = False

model = whisper.load_model("tiny", download_root=MODEL_HOME, in_memory=True)
if torch.cuda.is_available():
    model.cuda()
    GPU_SPEED_UP = True


@v2t.post("/", tags=["语音转文字"])
async def convert_voice_to_text(file: UploadFile = File(...)):
    # logging.debug(file)
    logging.debug(file.filename)
    file_name = file.filename
    file_bytes = await file.read()
    if not FileUtil.is_m4a(file_bytes) and not FileUtil.is_wav(file_bytes) and not FileUtil.is_mp3(file_bytes):
        logging.warning(f"validate failed: {file_name} is not a validate audio, only m4a or mp3 or wav accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.AUDIO_FILE_INVALIDATE, file_name)
        return result
    file_writer = open(USER_HOME+SysUtil.file_separator()+file_name, 'wb')
    file_writer.write(file_bytes)
    file_writer.close()

    audio = whisper.load_audio(USER_HOME+SysUtil.file_separator()+file_name)
    audio = whisper.pad_or_trim(audio)  # load audio and pad/trim it to 30 seconds, change length to 60 seconds and simple rate with 16000
    mel = whisper.log_mel_spectrogram(audio).to(model.device)  # pass to cuda
    # decode the audio
    options = whisper.DecodingOptions(fp16=GPU_SPEED_UP, language='zh', without_timestamps=True, task='transcribe')
    t1 = TimeUtil.unix_now()
    txt = whisper.decode(model, mel, options)
    t2 = TimeUtil.unix_now()
    logging.debug(f"v2t cost: {t2 - t1} ms")
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, txt.text)
    return result


@v2t.post("/v2", tags=["语音转文字"])
async def convert_voice_to_text2(file: UploadFile = File(...)):
    logging.debug(file.filename)
    file_name = file.filename
    file_bytes = await file.read()
    if not FileUtil.is_m4a(file_bytes) and not FileUtil.is_wav(file_bytes) and not FileUtil.is_mp3(file_bytes):
        logging.warning(f"validate failed: {file_name} is not a validate audio, only m4a or mp3 or wav accepted!")
        result = ReedResult.get(ReedV2T2VErrorCode.AUDIO_FILE_INVALIDATE, file_name)
        return result
    disk_file = USER_HOME + SysUtil.file_separator() + file_name
    file_writer = open(disk_file, 'wb')
    file_writer.write(file_bytes)
    file_writer.close()
    audio_file = AudioFile.get(disk_file)
    audio_file.filename = file_name
    # try:
    #     # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
    #     # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
    #     out, _ = (
    #         ffmpeg.input(disk_file, threads=0)
    #         .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=audio_file.sample_rate)
    #         .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    #     )
    # except ffmpeg.Error as e:
    #     raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
    # audio = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
    # audio = whisper.pad_or_trim(audio)  # load audio and pad/trim it to 30 seconds, change length to 60 seconds and simple rate with 16000
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)  # pass to cuda
    # decode the audio
    # options = whisper.DecodingOptions(fp16=False, language='zh', without_timestamps=True, task='transcribe')
    # txt = whisper.decode(model, mel, options)
    # options = whisper.DecodingOptions(fp16=False, language="zh", task="transcribe", without_timestamps=True)
    audio = disk_file
    t1 = TimeUtil.unix_now()
    audio_transcribe = model.transcribe(audio=audio, word_timestamps=False, fp16=GPU_SPEED_UP, language="zh", task="transcribe",
                           without_timestamps=True, initial_prompt=CHINESE_PROMPT)
    t2 = TimeUtil.unix_now()
    logging.debug(f"v2t cost: {t2 - t1} ms")
    r = dict()
    logging.debug(f"audio_transcribe:{audio_transcribe}")
    r["decode_result"] = audio_transcribe["text"]
    r["audio_info"] = audio_file
    logging.debug(r)
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, r)
    return result

