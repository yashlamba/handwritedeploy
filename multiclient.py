import asyncio
import aiohttp
import requests
import time


addr = "http://handwritetest.herokuapp.com"
# addr = "http://localhost:5000"
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
        async for x in make_numbers(1, 11):
            post_tasks.append(do_post(session, x))
        # now execute them all at once
        await asyncio.gather(*post_tasks)


async def do_post(session, i):
    async with session.post(test_url, data=data, headers=headers) as response:
        datares = await response.text()
        if "DOCTYPE" in datares:
            print("error in ", i)
            return
        print(datares)
        while True:
            time.sleep(2)
            # print(dat11ares)
            checkstatus = requests.get(
                addr + "/handwrite/" + eval(str(datares))["path"]
            )
            print(f"Status for {i} = {checkstatus.text}")
            if checkstatus.text == "Done":
                font = requests.post(addr + "/handwrite/fetch/" + eval(datares)["path"])
                # print(font.content)
                break

        # print("-> Created account number %d" % x)
        print(f"FETCHED {i}:", font.content[:5])
        # with open(f"new{i}.ttf", "wb+") as f:
        #     f.write(font.content)


loop = asyncio.get_event_loop()
loop.run_until_complete(make_account())
