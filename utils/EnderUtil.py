import json
import pathlib
import re
import sys
import time
import os
from datetime import datetime
import uuid

import pytz


class StringUtil(object):
    @staticmethod
    def isJson(source: str) -> bool:
        try:
            json.loads(source)
        except ValueError as e:
            return False
        return True

    @staticmethod
    def isEmpty(source: str) -> bool:
        if source is None:
            return True
        if type(source) == str and len(str(source).strip()) == 0:
            return True
        else:
            return False

    @staticmethod
    def isHttpUrl(url: str) -> bool:
        # pattern = re.compile('https?://([\w]+\.)+[\w]+(/[\w./?%&=]*)?$')
        pattern = re.compile("^(((ht|f)tps?):\/\/)?[\w-]+(\.[\w-]+)+([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?$")
        return re.match(pattern, url) != None


    @staticmethod
    def uuid(key: str = None) -> str:
        if StringUtil.isEmpty(key):
            return uuid.uuid1().__str__()
        else:
            return uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=key).__str__()



class TimeUtil(object):
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    @staticmethod
    def now() -> str:
        return datetime.now()

    @staticmethod
    def today() -> datetime:
        return datetime.now()

    @staticmethod
    def get_date(Y_m_d: str) -> datetime:
        return datetime.strptime(Y_m_d, "%Y-%m-%d")

    @staticmethod
    def get_datetime(Y_m_d_blank_H_M_S: str) -> datetime:
        return datetime.strptime(Y_m_d_blank_H_M_S, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def unix_now() -> int:
        return int(round(time.time() * 1000))

    @staticmethod
    def local_time_struct(timeStr: str) -> datetime:
        return time.localtime(int(timeStr) / 1000)

    @staticmethod
    def format_time_second(timeStr: str) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", TimeUtil.local_time_struct(timeStr))

    @staticmethod
    def format_time_milsecond(timeStr: str) -> str:
        milsecond = timeStr[-3:]
        return TimeUtil.format_time_second(timeStr) + ":" + milsecond

    @staticmethod
    def parse_time_second(timeStr: str) -> datetime:
        return datetime.strptime(TimeUtil.format_time_second(timeStr), "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_seconds(timeStr: str) -> int:
        return int(round(time.mktime(time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")))) * 1000

    @staticmethod
    def is_validate_timezone(timezone: str) -> bool:
        print(pytz.all_timezones)
        if not StringUtil.isEmpty(timezone):
            return timezone in pytz.all_timezones
        else:
            return False

    @staticmethod
    def is_validate_datetime(dt: str) -> bool:
        try:
            datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return False
        return True

    @staticmethod
    def is_validate_year(dt: int) -> bool:
        return True if 1900 <= dt <= 2099 else False

    @staticmethod
    def is_validate_month(dt: int) -> bool:
        return True if 1 <= dt <= 12 else False

    @staticmethod
    def is_validate_date(dt: str) -> bool:
        try:
            datetime.strptime(dt, "%Y-%m-%d")
        except Exception as e:
            return False
        return True

    @staticmethod
    def is_leap_year(year: int) -> bool:
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            return True
        return False

    @staticmethod
    def day_of_year(dt: datetime) -> int:
        year = dt.year
        month = dt.month
        day = dt.day
        result = 0
        for idx in range(len(TimeUtil.month_days)):
            if month > idx + 1:
                if not TimeUtil.is_leap_year(year) and idx == 1:
                    result += 28
                else:
                    result += TimeUtil.month_days[idx]
        return result + day

    @staticmethod
    def week_of_year(dt: datetime) -> int:
        return dt.isocalendar()[1] + 1

    @staticmethod
    def month_minus_day(dt: datetime) -> str:
        return "{}-{}".format(dt.month, dt.day)

    @staticmethod
    def get_days_index(dt: datetime) -> int:
        idx = -1
        for mIdx in range(dt.month - 1):
            idx += TimeUtil.month_days[mIdx]
        idx += dt.day
        if not TimeUtil.is_leap_year(dt.year) and dt.month > 2:
            idx -= 1
        return idx


class FileUtil:
    @staticmethod
    def is_mp3(file_bytes: bytes) -> bool:  # according to https://www.garykessler.net/library/file_sigs.html
        if len(file_bytes) <= 3:
            return False
        if file_bytes[0] == 0x49 and file_bytes[1] == 0x44 and file_bytes[2] == 0x33:
            return True
        elif file_bytes[0] == 0xff and file_bytes[1] == 0xfb:
            return True
        elif file_bytes[0] == 0xff and file_bytes[1] == 0xf3:
            return True
        elif file_bytes[0] == 0xff and file_bytes[1] == 0xf2:
            return True
        else:
            return False

    @staticmethod
    def is_wav(file_bytes: bytes) -> bool:  # according to https://www.garykessler.net/library/file_sigs.html
        if len(file_bytes) <= 16:
            return False
        if file_bytes[0] == 0x52 and file_bytes[1] == 0x49 and file_bytes[2] == 0x46 and file_bytes[3] == 0x46 and\
                file_bytes[8] == 0x57 and file_bytes[9] == 0x41 and file_bytes[10] == 0x56 and\
                file_bytes[11] == 0x45 and file_bytes[12] == 0x66 and file_bytes[13] == 0x6d and\
                file_bytes[14] == 0x74 and file_bytes[15] == 0x20:
            return True
        else:
            return False

    @staticmethod
    def is_m4a(file_bytes: bytes) -> bool:  # according to https://www.garykessler.net/library/file_sigs.html
        if len(file_bytes) <= 12:
            return False
        if file_bytes[4] == 0x66 and file_bytes[5] == 0x74 and file_bytes[6] == 0x79 and file_bytes[7] == 0x70 and \
                file_bytes[8] == 0x4d and file_bytes[9] == 0x34 and file_bytes[10] == 0x41 and \
                file_bytes[11] == 0x20:
            return True
        else:
            return False

class SysUtil:
    @staticmethod
    def get_os_env(key: str) -> str:
        return os.getenv(key)

    @staticmethod
    def get_os_platform() -> str:
        _os = sys.platform
        if _os.startswith("aix"):
            return "AIX"
        elif _os.startswith("linux"):
            return "LINUX"
        elif _os.startswith("win"):
            return "WINDOWS"
        elif _os.startswith("cygwin"):
            return "WINDOWS/CYGWIN"
        elif _os.startswith("darwin"):
            return "MACOS"
        else:
            return "UNKNOWN"

    @staticmethod
    def get_user_dir() -> str:
        return pathlib.Path.home().__str__()

    @staticmethod
    def file_separator() -> str:
        if SysUtil.get_os_platform() == "WINDOWS":
            return '\\'
        else:
            return '/'


    # print(TimeUtil.now())
    # print(TimeUtil.unix_now())
    # print(datetime.timestamp(datetime.now()))
    # print(calendar.timegm(time.gmtime()))
    # print(TimeUtil.format_time_second(TimeUtil.unix_now()))

    # print(TimeUtil.is_validate_datetime("1500-12-11 11:11:11"))

# print(TimeUtil.local_time_struct(time.time()*1000))
# print(time.strptime("2022-08-24 16:12:55", "%Y-%m-%d %H:%M:%S"))
# print(time.mktime(time.strptime("2022-08-24 16:12:55", "%Y-%m-%d %H:%M:%S")))
# print(TimeUtil.get_seconds("2022-08-24 16:12:55"))
# print(TimeUtil.unix_now()
# print(TimeUtil.format_time_second("1661328775000"))
# print(TimeUtil.day_of_year(TimeUtil.today()))
# print(TimeUtil.week_of_year(TimeUtil.today()))
# print(TimeUtil.month_minus_day(TimeUtil.get_date("2022-05-03")))

# print(TimeUtil.get_days_index(TimeUtil.get_date("2024-3-8")))
# print(StringUtil.isEmpty(None))
# print(StringUtil.uuid())
# print(StringUtil.uuid())
# print(StringUtil.uuid())
# print(StringUtil.uuid("ender"))
# print(StringUtil.uuid("ender"))
# print(StringUtil.uuid("ender"))
# print(StringUtil.isHttpUrl("http://127.0.0.1:5000/test/ender"))

# print(SysUtil.get_os_env("HOME"))
# print(SysUtil.get_os_platform())
# print(SysUtil.get_user_dir())