from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

import markdown2

import random


def index(request):
    if request.method == "POST":
        entry = request.POST['q']
        entries = util.list_entries()
        new = []
        for e in entries:
            e = e.lower()
            new.append(e)
        entry = entry.lower()
        if entry in new:
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
        else:
            arr=[]
            for n in new:
                if entry in n:
                    arr.append(n)
            return render(request, "encyclopedia/search.html", {
                "entry":entry,
                "entries": arr,
                "head": random.choice(util.list_entries())
            })
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "head": random.choice(util.list_entries())
    })

def entry(request, title):
    if (util.get_entry(title)) != None:
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "entry": markdown2.markdown(util.get_entry(title)),
            "head": random.choice(util.list_entries())
        })
    message = "Entry not found"
    return render(request, "encyclopedia/error.html",{
        "error":message,
        "head": random.choice(util.list_entries())
    })

def new(request):
    if request.method == "POST":
        title = request.POST['title']
        if not title:
            message = "Specify title"
            return render(request, "encyclopedia/error.html",{
                "error":message,
                "head": random.choice(util.list_entries())
            })
        entries = util.list_entries()
        new = []
        for e in entries:
            e = e.lower()
            new.append(e)
        title = title.lower()
        if title in new:
            message="Entry already exists :("
            return render(request, "encyclopedia/error.html",{
                "error":message,
                "head": random.choice(util.list_entries())
            })
        else:
            body = request.POST['body']
            if not body:
                message="Specify content :("
                return render(request, "encyclopedia/error.html",{
                    "error":message,
                    "head": random.choice(util.list_entries())
                })
            util.save_entry(request.POST['title'], body)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "entry": markdown2.markdown(util.get_entry(title)),
                "head": random.choice(util.list_entries())
            })
    return render(request, "encyclopedia/new.html",{
        "head": random.choice(util.list_entries())
    })

def edit(request, title):
    if request.method == "POST":
        body = request.POST['body']
        util.save_entry(title, body)
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "entry": markdown2.markdown(util.get_entry(title)),
            "head": random.choice(util.list_entries())
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": util.get_entry(title),
        "head": random.choice(util.list_entries())
    })