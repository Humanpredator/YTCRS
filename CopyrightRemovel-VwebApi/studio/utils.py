from typing import Union, List


def get_nested_key(d: Union[dict, List[dict]], key: str, default="UNKNOWN") -> Union[str, dict, List[str]]:
    if isinstance(d, list):
        for item in d:
            result = get_nested_key(item, key)
            if result is not None:
                return result
    elif isinstance(d, dict):
        for k, v in d.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = get_nested_key(v, key)
                if result is not None:
                    return result
    return default


def format_ms_to_time(ms):
    seconds = ms / 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
