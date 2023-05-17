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
        codec_name = stream.get("codec_name") if stream.get("codec_name") is not None else "unknown"
        codec_long_name = stream.get("codec_long_name") if stream.get("codec_long_name") is not None else "unknown"
        sample_fmt = stream.get("sample_fmt") if stream.get("sample_fmt") is not None else "unknown"
        sample_rate = int(stream.get("sample_rate") if stream.get("sample_rate") is not None else -1)
        audio_format = info["format"]
        filename = audio_format.get("filename")
        size = int(audio_format.get("size") if audio_format.get("size") is not None else -1)
        start_time = float(audio_format.get("start_time") if audio_format.get("start_time") is not None else -1)
        duration = float(audio_format.get("duration") if audio_format.get("duration") is not None else -1)
        bit_rate = int(audio_format.get("bit_rate") if audio_format.get("bit_rate") is not None else -1)
        if audio_format.get("tag"):
            creation_time = datetime.strptime(audio_format["tags"]["creation_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            encoder = audio_format["tags"]["encoder"]
        else:
            creation_time = "unknown"
            encoder = "unknown"

        return cls(filename=filename, size=size, start_time=start_time, duration=duration, bit_rate=bit_rate,
                   creation_time=creation_time, encoder=encoder, codec_name=codec_name,
                   codec_long_name=codec_long_name, sample_fmt=sample_fmt, sample_rate=sample_rate)

