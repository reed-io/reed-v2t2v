import ffmpeg
from datetime import datetime
from pydantic import BaseModel

class AudioFile(BaseModel):
    filename: str
    size: int
    start_time: float
    duration: float
    bit_rate: int
    creation_time: datetime
    encoder: str
    codec_name: str
    codec_long_name: str
    sample_fmt: str
    sample_rate: int

    @classmethod
    def get(cls, file):
        info = ffmpeg.probe(filename=file)
        streams = info["streams"]
        if len(streams) != 1:
            raise Exception(f"invalidate stream detected in {file}")
        stream = streams[0]
        audio_format = info["format"]
        filename = audio_format["filename"]
        size = int(audio_format["size"])
        start_time = float(audio_format["start_time"])
        duration = float(audio_format["duration"])
        bit_rate = int(audio_format["bit_rate"])
        creation_time = datetime.strptime(audio_format["tags"]["creation_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
        encoder = audio_format["tags"]["encoder"]
        codec_name = stream["codec_name"]
        codec_long_name = stream["codec_long_name"]
        sample_fmt = stream["sample_fmt"]
        sample_rate = stream["sample_rate"]

        return cls(filename=filename, size=size, start_time=start_time, duration=duration, bit_rate=bit_rate,
                   creation_time=creation_time, encoder=encoder, codec_name=codec_name,
                   codec_long_name=codec_long_name, sample_fmt=sample_fmt, sample_rate=sample_rate)

