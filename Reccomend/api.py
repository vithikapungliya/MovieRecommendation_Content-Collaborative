import requests
import imdb
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
KEY = 'fce8d58c194c55d32f7deb81e406692c'


def get_image_api(movie):
    try:
        ia = imdb.IMDb()
        search = ia.search_movie(movie)
        id = search[0].movieID
        id="tt"+id

        url = CONFIG_PATTERN.format(key=KEY)
        r = requests.get(url)
        config = r.json()

        base_url = config['images']['base_url']
        sizes = config['images']['poster_sizes']
        """
            'sizes' should be sorted in ascending order, so
                max_size = sizes[-1]
            should get the largest size as well.        
        """
        def size_str_to_int(x):
            return float("inf") if x == 'original' else int(x[1:])

        max_size = max(sizes, key=size_str_to_int)

        IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
        r = requests.get(IMG_PATTERN.format(key=KEY,imdbid=id)) #Movie Title 
        api_response = r.json()
        # print(api_response)

        posters = api_response['posters']
        poster_urls = []
        for poster in posters:
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(base_url, max_size, rel_path)
            poster_urls.append(url)

        return poster_urls[0]    
    except:
        return None
