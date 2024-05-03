import asyncio
import aiohttp
from collections import defaultdict, Counter


async def _fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def _get_top_stories(session):
        top_ids = await _fetch(session, 'https://hacker-news.firebaseio.com/v0/topstories.json')
        return top_ids

async def _get_item_details(session, item_id):
    story_details = await _fetch(session, f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json')
    return story_details


async def get_comments(limit_comments=50, limit_top_stories=100):
    res = defaultdict(list)

    async with aiohttp.ClientSession() as session:
        top_ids = await _get_top_stories(session)
        top_ids = top_ids[:limit_top_stories]

        tasks = []
        for story_id in top_ids:
            print(f'story: {story_id}')
            story_details_task = asyncio.create_task(_get_item_details(session, story_id))
            tasks.append(story_details_task)

        story_details_results = await asyncio.gather(*tasks)

        for story_details in story_details_results:
            comment_ids = story_details.get('kids', [])
            comment_ids = comment_ids[:limit_comments]

            comment_tasks = [asyncio.create_task(_get_item_details(session, comment_id)) for comment_id in comment_ids]
            comments = await asyncio.gather(*comment_tasks)

            for comment in comments:
                print(f'  comment: {comment.get("id")}')
                res[story_details.get('id')].append(comment.get('text'))

    return res

async def _process_comment(comment, counter):
    if comment:
        text = comment.get('text', '')
        words = text.split()
        counter.update(words)
    else:
        print("Comment is None")


async def get_most_used_words(limit_comments=100, limit_top_stories=30, limit_most_common=10):
    async with aiohttp.ClientSession() as session:
        top_ids = await _get_top_stories(session)
        top_ids = top_ids[:limit_top_stories]

    counter_list = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for story_id in top_ids:
            # print(f'story: {story_id}')
            story_details_task = asyncio.create_task(_get_item_details(session, story_id))
            tasks.append(story_details_task)
                
        story_details_results = await asyncio.gather(*tasks)

        #TODO change later, shouldnt use a for here
        for story_details in story_details_results:
            comment_ids = story_details.get('kids', [])
            comment_ids = comment_ids[:limit_comments]
            for comment_id in comment_ids:
                # print(f'  comment: {comment_id}')
                comment = await _get_item_details(session, comment_id)

                if comment:
                    text = comment.get('text', '')
                    words = text.split()
                    counter_list.append(Counter(words))
                else:
                    print("Comment is None")

    total_counter = sum(counter_list, Counter())
    res = total_counter.most_common(limit_most_common)
    return res




async def _get_nested_comment_ids(session, item_id, comment_ids=None):
    if comment_ids is None:
        comment_ids = []

    item_details = await _get_item_details(session, item_id)
    kids = item_details.get('kids', [])
    comment_ids.extend(kids)
    
    tasks = [asyncio.create_task(_get_nested_comment_ids(session, child_id, comment_ids)) for child_id in kids]
    await asyncio.gather(*tasks)

    return comment_ids

async def _count_words_nested(story_id, session):
    counter = Counter()
    comment_ids = await _get_nested_comment_ids(session, story_id)

    tasks = [asyncio.create_task(_get_item_details(session, comment_id)) for comment_id in comment_ids]
    comments = await asyncio.gather(*tasks)
    
    processing_tasks = [asyncio.create_task(_process_comment(comment, counter)) for comment in comments]
    
    await asyncio.gather(*processing_tasks)
    
    return counter

async def get_most_used_words_with_nested_comments(limit_top_stories=10, limit_most_common: None|int=None):

    async with aiohttp.ClientSession() as session:
        top_ids = await _get_top_stories(session)
        top_ids = top_ids[:limit_top_stories]

        counters = await asyncio.gather(*[_count_words_nested(story_id, session) for story_id in top_ids])
        total_counter = sum(counters, Counter())
        res = total_counter.most_common(limit_most_common)
    return res
