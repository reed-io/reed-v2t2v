from paddlespeech.cli.asr.infer import ASRExecutor

asr = ASRExecutor()
result = asr(audio_file="/home/ender/reed_tts.m4a")
print(result)