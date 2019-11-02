import asyncio
import random
from time import time



# asyncio works by gathering tasks (coroutines, futures) and then running an event loop
# When a task is blocked waiting for some io, the next task is then allowed to execute
# until it is blocked, and so on. The return of the event loop is a list of the return
# values of each of the coroutines. All results are returned at the same time after the
# longest running coroutine is complete. This is much faster than waiting for each to 
# complete in turn.

async def coro(id: int) -> str:  # coroutine that would go and get some data
    t = random.randint(1,5)
    await asyncio.sleep(t)  # would await some response IRL
    return f'coroutine {id} done after {t}s', t

async def main() -> asyncio.Future:  # coroutine which gathers tasks, awaits completion, and returns the result
    tasks = []
    for i in range(5):
        tasks.append(asyncio.create_task(coro(i)))
        
    return await asyncio.gather(*tasks) # returns a future aggregating the tasks' results
    #  only returns after coroutines all finish


start = time()
r = asyncio.run(main()) # runs the main() future and returns its agg of coroutine results
end = time()

r, t = zip(*r)

for result in r:
    print(result)

print(f'executed in {round(end - start)}s')
print(f'would have taken {sum(t)}s synchronously')



#  EXAMPLE OF HTTP REQUEST USING AIOHTTP (uses lower level loop):

# import aiohttp
# import asyncio

# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()

# async def main():
#     urls = [
#             'http://python.org',
#             'https://google.com',
#             'http://yifei.me'
#         ]
#     tasks = []
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             tasks.append(fetch(session, url))
#         htmls = await asyncio.gather(*tasks)
#         for html in htmls:
#             print(html[:100])

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
