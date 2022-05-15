from decouple import config


class BaseConfig:
    CACHE_TYPE = config('CACHE_TYPE')
    CACHE_REDIS_HOST = config('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = config('CACHE_REDIS_PORT')
    CACHE_REDIS_DB = config('CACHE_REDIS_DB')
    CACHE_REDIS_URL = config('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = config('CACHE_DEFAULT_TIMEOUT')