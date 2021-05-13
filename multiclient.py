import asyncio
import aiohttp


addr = "http://handwritetest.herokuapp.com"
test_url = addr + "/handwrite/test"
content_type = "image/jpeg"
headers = {"content-type": content_type}
data = open("excellent2.jpg", "rb").read()


async def make_numbers(numbers, _numbers):
    for i in range(numbers, _numbers):
        print(i)
        yield i


async def make_account():
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        # prepare the coroutines that post
        async for x in make_numbers(1, 6):
            post_tasks.append(do_post(session, x))
        # now execute them all at once
        await asyncio.gather(*post_tasks)


async def do_post(session, i):
    async with session.post(test_url, data=data, headers=headers) as response:
        datares = await response.content.read()
        # print("-> Created account number %d" % x)
        with open(f"new{i}.ttf", "wb+") as f:
            f.write(datares)

loop = asyncio.get_event_loop()
loop.run_until_complete(make_account())
