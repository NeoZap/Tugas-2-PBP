from django.shortcuts import render
from katalog.models import CatalogItem

def show_katalog(request):
    context = {
        "item_catalog": CatalogItem.objects.all(),
        "name": "Aushaaf Fadhilah Azzah",
        "npm": "2106630063"
    }
    return render(request, "katalog.html", context)
