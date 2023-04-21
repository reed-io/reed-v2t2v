import ffmpeg

info = ffmpeg.probe(filename="d:\\北街家园七区.m4a")
print(info["streams"][0]["sample_rate"])