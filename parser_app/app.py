import asyncio
import faust
import uuid
import aiohttp
from . import constants
from parser_app.schemas import UUIDParam, CategoryParam

app = faust.App(
    'myapp',
    broker='kafka://localhost:29092',
    topic_replication_factor=1,
    topic_partitions=1,
    topic_allow_declare=True,
    auto_discover=True
)

ParserTopic = app.topic("api-parser", value_type=CategoryParam, key_type=str)
GlobTable = app.GlobalTable("results-table", default=list, use_partitioner=True)


def save_to_glob_table(data, uuid_key):
    for i in data:
        product = {"title": i['title'],
                   "price": i['price']}
        old = GlobTable[uuid_key]
        old.append(product)
        GlobTable[uuid_key] = old


@app.task
async def start():
    await ParserTopic.maybe_declare()


@app.page('/search/')
async def get(web, request):
    uid = str(uuid.uuid4())
    await ParserTopic.send(key=uid, value=CategoryParam(q=request.query["q"]))
    return web.json({"uuid": uid})


@app.page('/result/')
async def get(web, request):
    uid: UUIDParam[str] = request.query["q"]
    return web.json({"results": GlobTable[uid]})


@app.agent(ParserTopic)
async def get_data_from_fakestore_api(stream):
    async for uuid_key, category in stream.items():
        async with aiohttp.ClientSession() as session:
            async with session.get(constants.FAKESTOREAPI_URL + constants.FAKESTORE_REQUEST_MAPPER[category.q]) as resp:
                data = await resp.json()
                await asyncio.sleep(15)
                save_to_glob_table(data, uuid_key)


@app.agent(ParserTopic)
async def get_data_from_dummystore_api(stream):
    async for uuid_key, category in stream.items():
        async with aiohttp.ClientSession() as session:
            async with session.get(constants.DUMMYSTORE_URL + constants.DUMMYSTORE_REQUEST_MAPPER[category.q]) as resp:
                data = await resp.json()
                await asyncio.sleep(10)
                save_to_glob_table(data['products'], uuid_key)
