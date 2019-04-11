from django.shortcuts import render
from django.db import connection
from KYS.forms import search_bar
from show.models import Show
from show.models import language
from .models import cast

# Create your views here.

def Cast(request,id):
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
    actor = cast.objects.raw('''
        SELECT * FROM cast_cast
        WHERE id=%s
        ;
    ''',[id,])
    castActedMovies = Show.objects.raw('''
        SELECT *,EXTRACT(YEAR FROM releaseDate) AS year FROM show_show
        WHERE id in (SELECT show_id FROM show_show_cast WHERE cast_id=%s)
        ORDER BY releaseDate DESC;
    ''',[id])
    castProfession = cast.objects.raw('''
        SELECT * FROM cast_profession
        where id in (select profession_id from cast_cast_profession where cast_id=%s);
    ''',[id])
    form = search_bar()
    context = {
        'Cast':actor[0],
        'search_form':form,
        'moviesActed':castActedMovies,
        'castProfession':castProfession,
    }
    return render(request,'cast.html',context)
