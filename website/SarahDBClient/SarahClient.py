import requests
from . import encrypt
from . import __trash
import asyncio
import aiohttp
from functools import lru_cache
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CON_KEY = encrypt.decrypter(encrypt.decrypter(encrypt.decrypter(encrypt.decrypter((__trash.retTr())))))
from_ = "https://sarahdb.pythonanywhere.com"
# from_ = "http://127.0.0.1:781"
link_prefix = f"{from_}/{CON_KEY}/handler"
DB_URL = f"{from_}/login/{CON_KEY}"

# Connection pool
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))

# Asynchronous session
async_session = None

async def get_async_session():
    global async_session
    if async_session is None:
        async_session = aiohttp.ClientSession()
    return async_session

@lru_cache(maxsize=128)
def cached_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error in cached_request: {e}")
        return None

async def async_request(url):
    try:
        async with await get_async_session() as session:
            async with session.get(url) as response:
                return await response.text()
    except aiohttp.ClientError as e:
        logger.error(f"Error in async_request: {e}")
        return None

class dbORM:
    @staticmethod
    async def all():
        return await async_request(f'{link_prefix}/handler')

    @staticmethod
    @lru_cache(maxsize=32)
    def get_all(model):
        return cached_request(f'{link_prefix}/get_all/{model}')

    @staticmethod
    async def find_all(model, column, value):
        return await async_request(f'{link_prefix}/find_all/{model}/{column}/{value}')

    @staticmethod
    async def add_one(model, column, value):
        return await async_request(f'{link_prefix}/add_one/{model}/{column}/{value}')

    @staticmethod
    async def add_entry(model, column_value_pairs):
        try:
            return await async_request(f'{link_prefix}/add_entry/{model}/{column_value_pairs}')
        except Exception as e:
            logger.error(f"Error in add_entry: {e}, model: {model}, cvp: {column_value_pairs}")
            return None

    @staticmethod
    @lru_cache(maxsize=64)
    def find_one(model, column, value):
        return cached_request(f'{link_prefix}/find_one/{model}/{column}/{value}')

    @staticmethod
    async def update_one(model, column, value_search, value_update):
        return await async_request(f'{link_prefix}/update_one/{model}/{column}/{value_search}/{value_update}')

    @staticmethod
    async def update_entry(model, column, column_value_pairs, dnd):
        if dnd:
            data = {
                "model": f"{model}", 
                "column": f"{column}", 
                "cvp": f"{column_value_pairs}"
            }
            async with await get_async_session() as session:
                async with session.post(f'{link_prefix}/update_entry_dnd', data=data) as response:
                    return await response.text()
        else:
            return await async_request(f'{link_prefix}/update_entry/{model}/{column}/{column_value_pairs}')

    @staticmethod
    async def delete_entry(model, column):
        return await async_request(f'{link_prefix}/delete_entry/{model}/{column}')

    @staticmethod
    def sanitize_string(string):
        return str(string.replace("'", "").replace('"', ''))

try:
    response = session.get(DB_URL)
    response.raise_for_status()
    logger.info("Connected to db server successfully")
    logger.debug(f"Response: {response.text}")
except requests.RequestException as e:
    logger.error(f"Error connecting to db server: {e}")
    dbORM = None

# Cleanup function
async def cleanup():
    if async_session:
        await async_session.close()

# Make sure to call this when your application shuts down
# asyncio.get_event_loop().run_until_complete(cleanup())

