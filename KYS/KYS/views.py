from django.shortcuts import render
from django.db import connection
from .forms import search_bar
from show.models import Show
from cast.models import cast


def search(request):
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
        SELECT * FROM show_show;
    ''')
    movies_telugu = Show.objects.raw('''
        SELECT * FROM show_show
        WHERE id in (SELECT show_id FROM show_show_language WHERE language_id in (SELECT id FROM show_language WHERE languages="Telugu"));
        ;
    ''')

    form = search_bar()
    context = {
        'search_form':form,
        'movies':movies,
        'movies_telugu':movies_telugu,
    }

    return render(request,'KYS/homePage.html',context)
