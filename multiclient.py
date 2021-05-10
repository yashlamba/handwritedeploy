import asyncio
import aiohttp


addr = "http://handwritetest.herokuapp.com/"
test_url = addr + "/handwrite/test"
content_type = "image/jpeg"
headers = {"content-type": content_type}
data = open("excellent2.jpg", "rb").read()


async def get(session: aiohttp.ClientSession) -> dict:
    resp = await session.request(
        "POST", url=testurl, data=data, headers=headers
    )
    dataresp = await resp.status
    print("Received data for {url}")
    return resp


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for  in range(10):
            tasks.append(get(session=session))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        print(tasks)

        return htmls


if name == "main":
    asyncio.run(main())