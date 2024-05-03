# assignment-ecorushome
To run the application:

intall libraries: pip install -r requirements.txt
run: uvicorn app:app --reload


routes:
/top/comments
/top/words
/top/words/nested


# Things I couldn't do
The route names are a bit weird, I didn't have the time to properly setup query parameters like I wanted, but they should work.

I took a lot of time to implement the async functionality, and got a bit confused for the second one, so didn't have time to implement that one.
Routes 1 and 3 should be way faster, because I properly implemented the async functionality.

I didn't have the time to clean the text from the comments, but would be a good thing to add (for both the first route and for the word count)


# What I plan on doing in order

1. I'll first try to work with HN api and get a feel for it
2. After that, I'll add my own api and implement each of the routes / functionality
3. If I have the time, I'll try to add some testing, but I'll leave it for the end of the assignment.

4. The first version of the api should be working / almost completed now, I can try to work on:
    - async reads
    - clean comment text?
    - Adding caching to the system
    - make the api more modular - example: you can filter how many post to look (and only cache the information requested?)