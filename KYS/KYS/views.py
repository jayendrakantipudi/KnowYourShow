from django.shortcuts import render
from django.db import connection
from .forms import search_bar
from show.models import Show
from cast.models import cast
from django.shortcuts import redirect

def mainpage(request):
    list_of_movies=[]
    movies = Show.objects.raw('''
        SELECT * FROM show_show;
    ''')

    list_of_movies.append(["Movies",movies])
    movies_telugu = Show.objects.raw('''
        SELECT * FROM show_show
        WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="Telugu"));
        ;
    ''')

    list_of_movies.append(["Telugu Movies", movies_telugu])
    movies_english = Show.objects.raw('''
        SELECT * FROM show_show
        WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="English"));
        ;
    ''')

    list_of_movies.append(["Engish Movies", movies_english])
    movies_tamil = Show.objects.raw('''
            SELECT * FROM show_show
            WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="Tamil"));
            ;
        ''')

    list_of_movies.append(["Tamil Movies", movies_tamil])
    movies_malyalam = Show.objects.raw('''
                SELECT * FROM show_show
                WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="Malyalam"));
                ;
            ''')

    list_of_movies.append(["Malyalam Movies", movies_malyalam])
    movies_hindi = Show.objects.raw('''
                    SELECT * FROM show_show
                    WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="Hindi"));
                    ;
                ''')

    list_of_movies.append(["Hindi Movies", movies_hindi])
    movies_horror = Show.objects.raw('''
                        select * from show_show where id in(select show_id from show_show_genre where genre_id in (select id from show_genre where genres="Horror"));
                        ;
                    ''')

    list_of_movies.append(["Horror Movies", movies_horror])
    movies_comedy = Show.objects.raw('''
                            select * from show_show where id in(select show_id from show_show_genre where genre_id in (select id from show_genre where genres="Comedy"));
                            ;
                        ''')

    list_of_movies.append(["Comedy Movies", movies_comedy])
    movies_suspense= Show.objects.raw('''
                                select * from show_show where id in(select show_id from show_show_genre where genre_id in (select id from show_genre where genres="Suspense"));
                                ;
                            ''')

    list_of_movies.append(["Suspense Movies", movies_suspense])
    movies_thriller = Show.objects.raw('''
                                select * from show_show where id in(select show_id from show_show_genre where genre_id in (select id from show_genre where genres="Thriller"));
                                ;
                            ''')

    list_of_movies.append(["Thriller Movies", movies_thriller])
    movies_drama = Show.objects.raw('''
                                select * from show_show where id in(select show_id from show_show_genre where genre_id in (select id from show_genre where genres="Drama"));
                                ;
                            ''')

    list_of_movies.append(["Drama Movies", movies_drama])
    form = search_bar()

    context = {
        # 'search_form':form,
        # 'movies':movies,
        # 'movies_telugu':movies_telugu,
        # 'movies_english':movies_english,
        # 'movies_tamil': movies_tamil,
        # 'movies_malyalam': movies_malyalam,
        # 'movies_hindi': movies_hindi,
        # 'movies_horror':movies_horror,
        'search_form':form,
        'list_of_movies':list_of_movies,
    }

    return render(request,'KYS/homePage.html',context)


def search(request):
    if request.method == 'POST':
        form = search_bar(request.POST)
        if form.is_valid():
            search_list = ['titleName', 'storyLine']
            search_query = form.cleaned_data['search_query']
            search_ty = form.cleaned_data['search_ty']
            all_searches = []
            if search_ty == 'movies':
                all_shows_with_query = Show.objects.raw('''
                               SELECT *, EXTRACT(YEAR FROM releaseDate) AS year,LOCATE(%s,titleName)
                               FROM show_show
                               WHERE locate(%s,titleName)>0;
                   ''', [search_query, search_query])

                for i in all_shows_with_query:
                    all_searches.append(i)

                all_shows_with_query1 = Show.objects.raw('''
                           SELECT *, EXTRACT(YEAR FROM releaseDate) AS year,LOCATE(%s,storyLine)
                           FROM show_show
                           WHERE locate(%s,storyLine)>0;
                   ''', [search_query, search_query])
                for i in all_shows_with_query1:
                    all_searches.append(i)

                all_searches = set(all_searches)

                for i in all_searches:
                    print(i)

                if all_searches:
                    key=True

                else:
                    key=False
                form=search_bar()
                context = {
                              'all_searches': all_searches, 'key': key,
                    'search_query': search_query,
                    'search_form':form
                }
                return render(request, 'KYS/search_result.html', context)

            else:
                all_shows_with_query = cast.objects.raw('''
                               SELECT *, LOCATE(%s,name)
                               FROM cast_cast
                               WHERE locate(%s,name)>0;
                   ''', [search_query, search_query])

                for i in all_shows_with_query:
                    print(i, ' hello')

                if all_shows_with_query:
                    key=True
                else:
                    key=False
                print(search_query)
                form=search_bar()
                context = {
                    'all_shows_with_query': all_shows_with_query,
                    'key':key,
                    'search_query' : search_query,
                    'search_form':form,
                }
                return render(request, 'KYS/search_result.html', context)
    form = search_bar()
    context = {
        'search_form':form,
    }
    return render(request,'KYS/homePage.html',context)
