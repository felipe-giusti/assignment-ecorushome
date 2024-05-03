from fastapi import APIRouter, Query
from .hacker_news import utils


router = APIRouter()


@router.get("/top/comments")
async def get_comments_from_top_posts(limit_comments: int = Query(50, ge=1),
                                    limit_top_stories: int = Query(100, ge=1)):
    comments = await utils.get_comments(limit_comments, limit_top_stories)

    return comments


@router.get("/top/words")
async def get_word_count(limit_comments: int = Query(100, ge=1),
                        limit_top_stories: int = Query(30, ge=1),
                        limit_most_common: int = Query(10, ge=1)):
    
    word_count = await utils.get_most_used_words(limit_comments, limit_top_stories, limit_most_common)

    return word_count

# for simplicity I'm adding it to the path, I would prefer to add as a query parameter but wouldn't be able to set default values
@router.get("/top/words/nested")
async def get_word_count(limit_top_stories: int|None = Query(None, ge=1),
                        limit_most_common: int = Query(10, ge=1)):
    
    word_count = await utils.get_most_used_words_with_nested_comments(limit_top_stories, limit_most_common)

    return word_count
