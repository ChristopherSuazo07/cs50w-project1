from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
import random
from django.contrib import messages
import requests



def convertidor(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    
    if not content:
        return None
    else:
        return markdowner.convert(content)
    

def index(request):
    if request.method == "GET": 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            
        } )
    else:
        eliminar = request.POST
        print(eliminar['title'])
        util.delete_entry(eliminar['title'])
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            
        } )
    
def wiki(request, title):
    
    if request.method == "GET":
        
        entrada = util.get_entry(title)      
        contenido = convertidor(title)
        
        
        if not entrada:
            return render(request, "encyclopedia/error.html")
        
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "contenido": contenido
        })
        

def new(request):
    # save = util.save_entry(title, content)
    if request.method == "POST":
        form = request.POST
        
        if not form['new_title'] in util.list_entries():
            util.save_entry(form['new_title'], form['new_content'])
            return redirect("wiki", title = form['new_title'])
        else:
            messages.error(request, "La entrada que desea registrar ya existe, favor intente con un título diferente")
            return redirect("new")
            
      
    return render(request, "encyclopedia/new.html")


def search(request):
    
    q = request.GET['q'].lower()
    
    if request.method == "GET":
        entries = [entry.lower() for entry in util.list_entries()]
        
    if q in entries:
        return redirect('wiki', title=q)
    else:
        
        entradas = match(q)
        if entradas:
            return render(request, "encyclopedia/search.html",{
                "entradas":entradas
            })
        else:
            return render(request, "encyclopedia/search.html",{
                "n":1
            })


def match(q):
    result = []
    
    if not q:
        return result
    entries = util.list_entries()

    result = [i for i in entries if q.lower() in i.lower()]
    
    return result

def Random(request):
    if request.method == "GET":
        entradas = util.list_entries()
        
        if entradas:
            entry = random.choice(entradas)
            return redirect("wiki", title=entry)
        else:
            return redirect("index")    


def edit(request, title):
    
    if request.method == "GET":
        entry = util.get_entry(title)
        
        if not entry:
            return redirect("error")
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": entry
        })
    
    edited_entry = request.POST
    new_title = edited_entry['new_title']
    new_content = edited_entry['new_content']
    
    if new_title in util.list_entries():
        util.save_entry(title, new_content)
        return render(request, "encyclopedia/wiki.html",{
        "title": new_title,
        "contenido": convertidor(new_title)
    })
    else:
        util.nuevo(title,new_title)
        return render(request, "encyclopedia/wiki.html",{
            "title": new_title,
            "contenido": convertidor(new_title)
        })
    
    
def error(request, exception):
    return render(request,"encyclopedia/error.html")
