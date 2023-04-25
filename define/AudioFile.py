import ffmpeg
from datetime import datetime
from pydantic import BaseModel

class AudioFile(BaseModel):
    filename: str
    size: int
    start_time: float
    duration: float
    bit_rate: int
    creation_time: datetime | str = "unknown"
    encoder: str = "unknown"
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
        codec_name = stream.get("codec_name")
        codec_long_name = stream.get("codec_long_name")
        sample_fmt = stream.get("sample_fmt")
        sample_rate = stream.get("sample_rate")
        audio_format = info["format"]
        filename = audio_format.get("filename")
        size = int(audio_format.get("size"))
        start_time = float(audio_format.get("start_time"))
        duration = float(audio_format.get("duration"))
        bit_rate = int(audio_format.get("bit_rate"))
        if audio_format.get("tag"):
            creation_time = datetime.strptime(audio_format["tags"]["creation_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            encoder = audio_format["tags"]["encoder"]
        else:
            creation_time = "unknown"
            encoder = "unknown"

        return cls(filename=filename, size=size, start_time=start_time, duration=duration, bit_rate=bit_rate,
                   creation_time=creation_time, encoder=encoder, codec_name=codec_name,
                   codec_long_name=codec_long_name, sample_fmt=sample_fmt, sample_rate=sample_rate)

