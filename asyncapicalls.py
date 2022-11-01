import aiohttp
import asyncio

from parameters import *

async def get_item(session, url, headers):
    async with session.get(url, headers=headers) as resp:
        item = await resp.json()
        return item

async def bulk_get_itens(intended, api_url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for id in intended:
            url = base_url + api_url + str(id)
            tasks.append(asyncio.ensure_future(get_item(session, url, headers)))

        json_item_list = await asyncio.gather(*tasks)
        await session.close()
        return json_item_list