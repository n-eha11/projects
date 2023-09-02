import requests_with_caching

def get_movies_from_tastedive(name):
    d = {'q': name,'type' : 'movies','limit' : 5}
    movierecs = requests_with_caching.get("https://tastedive.com/api/similar", params=d)
    rec = movierecs.json()
    return rec
def extract_movie_titles(rec={}):
    movies = [x["Name"] for x in rec['Similar']['Results']]
    return movies
def get_related_titles(movies=[]):
    rel_movies = []
    for x in movies:
        prerel = extract_movie_titles(get_movies_from_tastedive(x))
        for j in prerel:
            if j not in rel_movies:
                rel_movies.append(j)
    return rel_movies

def get_movie_data(name):
    p = {'t': name,'r':'json'}
    premovieinfo = requests_with_caching.get('http://www.omdbapi.com/', params=p)
    movieinfo = premovieinfo.json()
    return movieinfo

def get_movie_rating(movieinfo={}):
    lst = movieinfo['Ratings']
    for x in lst:
        if x['Source'] != 'Rotten Tomatoes':
            rottentomato = 0 
        elif x['Source'] == 'Rotten Tomatoes':
            strrottentomato = movieinfo["Ratings"][lst.index(x)]['Value'].rstrip('%')
            rottentomato = int(strrottentomato)
            break 
        #print('printing x')
        #print(x)
        #if movieinfo["Ratings"][lst.index(x)]['Source'] == 'Rotten Tomatoes':
            #strrottentomato = movieinfo["Ratings"][lst.index(x)]['Value'].rstrip('%')
            #rottentomato = int(strrottentomato)
        #else: 
           # rottentomato = 0
    return rottentomato

def get_sorted_recommendations(wanttowatch=[]):
    master = {}
    firstpass = get_related_titles(wanttowatch)
    for x in firstpass:
        if x not in master:
            master[x] = get_movie_rating(get_movie_data(x))
    final = sorted(master, key=lambda x: (master[x], x), reverse=True)
    return final