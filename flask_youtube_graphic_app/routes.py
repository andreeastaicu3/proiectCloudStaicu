import requests
from isodate import parse_duration

from flask import Blueprint, render_template, current_app, request,redirect

main=Blueprint('main',__name__)


@main.route("/")
def home():
    return render_template('home.html')

@main.route('/youtube', methods=['GET','POST'])
def youtube():
    search_url='https://www.googleapis.com/youtube/v3/search'
    video_url='https://www.googleapis.com/youtube/v3/videos'
    
    videos=[]

    if request.method=='POST':

        search_params={
            'key':current_app.config['YOUTUBE_API_KEY'],
            'q':request.form.get('query'),
            'part':'snippet',
            'maxResults':6,
            'type':'video'
        }

        r=requests.get(search_url, params=search_params)
        #print(r.text)
        #test

        results=r.json()['items']

        #list of video ids    
        video_ids=[]
        for result in results:
            video_ids.append(result['id']['videoId'])


        if request.form.get('submit')=='lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')


        #se creaza un dictionar
        video_params = {
            'key':current_app.config['YOUTUBE_API_KEY'],
            'id':','.join(video_ids),
            'part':'snippet,contentDetails',
            'maxResults':6
        }

        r=requests.get(video_url,params=video_params)

        results=r.json()['items']

        
        for result in results:
            video_data={
                'id':result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail':result['snippet']['thumbnails']['high']['url'],
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'title':result['snippet']['title']
            }
            videos.append(video_data)
   
    return render_template('youtube.html',videos=videos)

@main.route("/books", methods=['GET','POST'])
def books():

    searchbooks_url='https://www.googleapis.com/books/v1/volumes'

    books=[]

    if request.method=='POST':

        searchbooks_params={
            'key':current_app.config['BOOK_API_KEY'],
            'q':request.form.get('query2'),
            #'q':'design',
            'part':'volumeInfo',
            'maxResults':6,
        }

        r=requests.get(searchbooks_url, params=searchbooks_params)

        #print(r.text)

        results=r.json()['items']

        
        #list of books ids    
        books_ids=[]
        for result in results:
            books_ids.append(result['id'])

        searchbook_params={
            'key':current_app.config['BOOK_API_KEY'],
            'id':','.join(books_ids),
            'part':'volumeInfo,title',
            'maxResults':6  
        }

        r=requests.get(searchbooks_url, params=searchbook_params)


        for result in results:
            book_data={
                'id':result['id'],
                'url':f'https://books.google.ro/books?id={result["id"]}',
                'thumbnail':result['volumeInfo']['imageLinks']['thumbnail'],
                'title':result['volumeInfo']['title'],
                #'author':result['volumeInfo']['authors']
            }
            books.append(book_data)

            #print(r.text)
        
        if request.form.get('submit')=='lucky':
            return redirect(f'https://books.google.ro/books?id={ books_ids[0] }')

    return render_template('books.html', books=books)
