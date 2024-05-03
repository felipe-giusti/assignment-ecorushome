from api.hacker_news import utils
import asyncio
from time import perf_counter


start = perf_counter()


asyncio.run(utils.get_most_used_words(10, 5))

# asyncio.run(utils.get_most_used_words_with_nested_comments(5))

stop = perf_counter()
print(f'{stop-start}')