from api.hacker_news.util import get_request
from collections import Counter, defaultdict



def third_endpoint_sync_logic():
    top_ids = get_request('/topstories.json')[:1]

    counter_list = []

    #maybe change later when I implement threading
    comment_ids = []

    def _get_nested_comment_ids(item_id):
            item_details = get_request(f'/item/{item_id}.json')
            for child_id in item_details.get('kids', []):
                comment_ids.append(child_id)
                _get_nested_comment_ids(child_id)

    for story_id in top_ids:
        print(f'story: {story_id}')
        _get_nested_comment_ids(story_id)
        
        for comment_id in comment_ids:
            print(f'  comment: {comment_id}')
            comment = get_request(f'/item/{comment_id}.json')
            text = comment.get('text')

            words = text.split()
            counter_list.append(Counter(words))

    counter = sum(counter_list, Counter())
    res = counter.most_common(10)

    print(res)




def second_endpoint_sync_logic():
    top_ids = get_request('/topstories.json')[:1]

    counter_list = []

    for story_id in top_ids:
        print(f'story: {story_id}')
        story_details = get_request(f'/item/{story_id}.json')
        for comment_id in story_details.get('kids', [])[:5]:
            print(f'  comment: {comment_id}')
            comment = get_request(f'/item/{comment_id}.json')
            text = comment.get('text')

            words = text.split()
            counter_list.append(Counter(words))

    counter = sum(counter_list, Counter())
    res = counter.most_common(10)

    print(res)




def first_endpoint_sync_logic():
    top_ids = get_request('/topstories.json')[:1]

    res = defaultdict(list)

    for story_id in top_ids:
        print(f'story: {story_id}')
        story_details = get_request(f'/item/{story_id}.json')
        for comment_id in story_details.get('kids', [])[:5]:
            print(f'  comment: {comment_id}')
            comment = get_request(f'/item/{comment_id}.json')
            
            res[story_id].append(comment.get('text'))

    print(res)