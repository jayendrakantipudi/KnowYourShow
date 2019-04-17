from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from .forms import genreForm,languageForm,show_update_form
from django.db import connection
from .models import language
from KYS.forms import search_bar
from show.models import Show
from cast.models import cast

# Create your views here.

def movie(request,id):
    user_rated = True
    user_review = Show.objects.raw('''
        SELECT * FROM show_review
        WHERE reviewer_id=%s AND show_id=%s;
    ''',[request.user.id,id])
    if not len(user_review):
        user_rated = False
    if request.method == 'POST':
        form = search_bar(request.POST)
        if form.is_valid():
            search_list =  ['titleName','storyLine']
            search_query = form.cleaned_data['search_query']
            search_ty = form.cleaned_data['search_ty']
            all_searches = []
            if search_ty == 'movies':
                all_shows_with_query = Show.objects.raw('''
                            SELECT id,titleName , LOCATE(%s,titleName)
                            FROM show_show
                            WHERE locate(%s,titleName)>0;
                ''',[search_query,search_query])

                for i in all_shows_with_query:
                    all_searches.append(i)


                all_shows_with_query1 = Show.objects.raw('''
                        SELECT id,titleName , LOCATE(%s,storyLine)
                        FROM show_show
                        WHERE locate(%s,storyLine)>0;
                ''',[search_query,search_query])
                for i in all_shows_with_query1:
                    all_searches.append(i)

                all_searches = set(all_searches)


                for i in all_searches:
                    print(i)
            else:
                all_shows_with_query = cast.objects.raw('''
                            SELECT id,name , LOCATE(%s,name)
                            FROM cast_cast
                            WHERE locate(%s,name)>0;
                ''',[search_query,search_query])

                for i in all_shows_with_query:
                    print(i)
    movies = Show.objects.raw('''
        SELECT *,EXTRACT(YEAR FROM releaseDate) AS year FROM show_show
        WHERE id=%s
        ;
    ''',[id,])

    form = search_bar()
    castActed = Show.objects.raw('''
        SELECT * FROM cast_cast
        WHERE id in (SELECT cast_id FROM show_show_cast WHERE show_id=%s);
        ;
    ''',[id])
    langs = Show.objects.raw('''
        SELECT * FROM show_language
        WHERE id in (SELECT language_id FROM show_show_language WHERE show_id=%s);
        ;
    ''',[id])
    genres = Show.objects.raw('''
        SELECT * FROM show_GENRE
        WHERE id in (SELECT  genre_id FROM show_show_GENRE WHERE show_id=%s);
        ;
    ''',[id])
    directors = cast.objects.raw('''
        SELECT * FROM cast_director
        WHERE id in (SELECT director_id FROM show_show_director WHERE show_id=%s);
    ''',[id])
    producers = cast.objects.raw('''
        SELECT * FROM cast_producer
        WHERE id in (SELECT producer_id FROM show_show_producer WHERE show_id=%s);
    ''',[id])
    reviews = Show.objects.raw('''
        SELECT *,username FROM show_review,auth_user
        WHERE show_review.show_id = %s AND show_review.reviewer_id = auth_user.id;
    ''',[id])
    avgRating =Show.objects.raw('''
        SELECT id,AVG(rating) AS KYSavg,COUNT(*) AS total FROM show_review
        WHERE show_id = %s;
    ''',[id])
    currentUser_review = Show.objects.raw('''
        SELECT * FROM show_review
        WHERE show_id = %s AND reviewer_id=%s;
    ''',[id,request.user.id])

    if not avgRating[0].KYSavg:
        context = {
            'show':movies[0],
            'search_form':form,
            'cast':castActed,
            'Genres' : genres,
            'Languages':langs,
            'reviews':reviews,
            'Directors':directors,
            'Producers':producers,
            'user_rated':user_rated,
            'RATING_INFO': False,
        }
    else:
        total_rating = round(avgRating[0].KYSavg,2)
        # if currentUser_review:
        #     temp = False
        # else:
        #     temp = currentUser_review[0],
        context = {
            'show':movies[0],
            'search_form':form,
            'cast':castActed,
            'Genres' : genres,
            'Languages':langs,
            'reviews':reviews,
            'Directors':directors,
            'Producers':producers,
            'user_rated':user_rated,
            'total_reviews':avgRating[0].total,
            'RATING_INFO': True,
            'KYSrating': total_rating,
            # 'user_review':temp,

        }
    return render(request,'show/movie.html',context)



def review_rate(request,id):
    if request.method == 'POST':
        try:
            Review = request.POST['Review']
        except MultiValueDictKeyError:
            Review = False
        try:
            rating = request.POST['rating']
        except MultiValueDictKeyError:
            rating = False
        user_review = Show.objects.raw('''
            SELECT * FROM show_review
            WHERE reviewer_id=%s AND show_id=%s;
        ''',[request.user.id,id])
        if not len(user_review):
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO show_review (rating,Review,reviewer_id,show_id)
                    VALUES(%s,%s,%s,%s);
                ''',[rating,Review,request.user.id,id])
    if request.method == 'POST':
        form = search_bar(request.POST)
        if form.is_valid():
            search_list =  ['titleName','storyLine']
            search_query = form.cleaned_data['search_query']
            search_ty = form.cleaned_data['search_ty']
            all_searches = []
            if search_ty == 'movies':
                all_shows_with_query = Show.objects.raw('''
                            SELECT id,titleName , LOCATE(%s,titleName)
                            FROM show_show
                            WHERE locate(%s,titleName)>0;
                ''',[search_query,search_query])

                for i in all_shows_with_query:
                    all_searches.append(i)


                all_shows_with_query1 = Show.objects.raw('''
                        SELECT id,titleName , LOCATE(%s,storyLine)
                        FROM show_show
                        WHERE locate(%s,storyLine)>0;
                ''',[search_query,search_query])
                for i in all_shows_with_query1:
                    all_searches.append(i)

                all_searches = set(all_searches)


                for i in all_searches:
                    print(i)
            else:
                all_shows_with_query = cast.objects.raw('''
                            SELECT id,name , LOCATE(%s,name)
                            FROM cast_cast
                            WHERE locate(%s,name)>0;
                ''',[search_query,search_query])

                for i in all_shows_with_query:
                    print(i)
    movies = Show.objects.raw('''
        SELECT *,EXTRACT(YEAR FROM releaseDate) AS year FROM show_show
        WHERE id=%s
        ;
    ''',[id,])

    form = search_bar()

    user_rated = True
    user_review = Show.objects.raw('''
        SELECT * FROM show_review
        WHERE reviewer_id=%s AND show_id=%s;
    ''',[request.user.id,id])
    if not len(user_review):
        user_rated = False

    castActed = Show.objects.raw('''
        SELECT * FROM cast_cast
        WHERE id in (SELECT cast_id FROM show_show_cast WHERE show_id=%s);
        ;
    ''',[id])
    langs = Show.objects.raw('''
        SELECT * FROM show_language
        WHERE id in (SELECT language_id FROM show_show_language WHERE show_id=%s);
        ;
    ''',[id])
    genres = Show.objects.raw('''
        SELECT * FROM show_GENRE
        WHERE id in (SELECT  genre_id FROM show_show_GENRE WHERE show_id=%s);
        ;
    ''',[id])
    directors = cast.objects.raw('''
        SELECT * FROM cast_director
        WHERE id in (SELECT director_id FROM show_show_director WHERE show_id=%s);
    ''',[id])
    producers = cast.objects.raw('''
        SELECT * FROM cast_producer
        WHERE id in (SELECT producer_id FROM show_show_producer WHERE show_id=%s);
    ''',[id])
    reviews = Show.objects.raw('''
        SELECT *,username FROM show_review,auth_user
        WHERE show_review.show_id = %s AND show_review.reviewer_id = auth_user.id;
    ''',[id])

    avgRating =Show.objects.raw('''
        SELECT id,AVG(rating) AS KYSavg,COUNT(*) AS total FROM show_review
        WHERE show_id = %s;
    ''',[id])
    currentUser_review = Show.objects.raw('''
        SELECT * FROM show_review
        WHERE show_id = %s AND reviewer_id=%s;
    ''',[id,request.user.id])

    if not avgRating[0].KYSavg:
        context = {
            'show':movies[0],
            'search_form':form,
            'cast':castActed,
            'Genres' : genres,
            'Languages':langs,
            'reviews':reviews,
            'Directors':directors,
            'Producers':producers,
            'user_rated':user_rated,
            'RATING_INFO': False,
        }
    else:
        total_rating = round(avgRating[0].KYSavg,2)
        context = {
            'show':movies[0],
            'search_form':form,
            'cast':castActed,
            'Genres' : genres,
            'Languages':langs,
            'reviews':reviews,
            'Directors':directors,
            'Producers':producers,
            'user_rated':user_rated,
            'total_reviews':avgRating[0].total,
            'RATING_INFO': True,
            'KYSrating': total_rating,
            'user_review':currentUser_review[0],
        }

    print()
    print()
    print(request.user.id)
    print(id)
    # print(rating)
    # print(Review)
    print()
    print()
    return render(request,'show/movie.html',context)




def language_form(request):
    if request.method == 'POST':
        lform = languageForm(request.POST)
        if lform.is_valid():
            lang = lform.cleaned_data['languages']
            print("\n\n",lang,"\n\n")
            with connection.cursor() as cursor:
                cursor.execute('''
                INSERT INTO show_language (languages)
                VALUES(%s);
        ''',[lang,])
    lform = languageForm()
    all_languages = language.objects.raw('''
        SELECT * FROM show_language;
    ''')
    return render(request,'show/language_form.html',{'lform':lform,'all_languages':all_languages})


def genre_form(request):
    if request.method == "POST":
        gform = genreForm(request.POST)
        if gform.is_valid():
            genre = gform.cleaned_data['genres']
            with connection.cursor() as cursor:
                cursor.execute('''
                INSERT INTO show_genre (genres)
                VALUES(%s);
        ''',[genre,])
    gform = genreForm()
    return render(request,'show/genre_form.html',{'gform':gform})

def update_show(request,movieID):
    if request.method == "POST":
        suform = show_update_form(request.POST)
        if suform.is_valid():
            tn = suform.cleaned_data['titleName']
            rd = suform.cleaned_data['releaseDate']
            sl = suform.cleaned_data['storyLine']
            bd = suform.cleaned_data['budget']
            boc = suform.cleaned_data['BoxOfficeCollection']
            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE show_show
                    SET titleName=%s,releaseDate=%s,storyLine=%s,budget=%s,BoxOfficeCollection=%s
                    WHERE id=%s;
                ''',[tn,rd,sl,bd,boc,movieID])
    suform = show_update_form()
    return render(request,'show/update_show.html',{'show_update_form':suform})
