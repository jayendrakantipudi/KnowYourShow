from django.shortcuts import render
from .forms import genreForm,languageForm,show_update_form
from django.db import connection
from .models import language
from KYS.forms import search_bar
from show.models import Show
from cast.models import cast

# Create your views here.

def movie(request,id):
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
        SELECT * FROM show_show
        WHERE id=%s
        ;
    ''',[id,])
    # print(movies[0].titleName)
    form = search_bar()
    year = movies[0].releaseDate.year
    castActed = Show.objects.raw('''
        SELECT * FROM show_show_cast
        WHERE show_id=%s
        ;
    ''',[id])
    castCrew= []
    for i in castActed:
        temp_cast = cast.objects.raw('''
            SELECT * FROM cast_cast
            WHERE id=%s;
        ''',[i.cast_id])
        castCrew.append(temp_cast[0])
    print()
    print()
    for i in castCrew:
        print(i.name)
        print()
        print()
    print()
    return render(request,'show/movie.html',{'show':movies[0],'search_form':form,'cast':castCrew,'Year':year})

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
