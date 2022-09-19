from django.shortcuts import render
from mywatchlist.models import MyWatchList
from django.http import HttpResponse
from django.core import serializers

def show_mywatchlist(request):
    mywatchlist = MyWatchList.objects.all()
    watched = 0
    for movie in mywatchlist:
        watched += movie.watched
    not_watched = len(mywatchlist)
    if watched >= not_watched:
        msg = "Selamat, kamu sudah banyak menonton!"
    else:
        msg = "Wah, kamu masih sedikit menonton!"

    context = {
        "mywatchlist": mywatchlist,
        "msg": msg,
    }
    
    return render(request, "mywatchlist.html", context)

def show_mywatchlist_json(request):
    mywatchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("json", mywatchlist), content_type="application/json")

def show_mywatchlist_xml(request):
    mywatchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", mywatchlist), content_type="application/xml")