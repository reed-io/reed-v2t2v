import whisper

model = whisper.load_model("tiny", in_memory=True)


# audio = whisper.load_audio("D:\\test.wav")
# audio = whisper.load_audio("d:\\北街家园七区.m4a")
# audio = whisper.pad_or_trim(audio)   # 把读取的音频进行对齐
# mel = whisper.log_mel_spectrogram(audio).to(model.device)  # log mel 音频特征提取
#
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")
# # decode the audio
# options = whisper.DecodingOptions(fp16=False)
# result = whisper.decode(model, mel, options)

prompt='以下是普通话的句子'
options = whisper.DecodingOptions(fp16=False, language="zh", task="transcribe", without_timestamps=True, initial_prompt=prompt)
result = model.transcribe(audio="d:\\北街家园七区.m4a", word_timestamps=False)

# prompt='以下是普通话的句子'
# result = model.transcribe(audioFile, task='translate',language='zh',verbose=True,initial_prompt=prompt)

# print the recognized text
print(result)