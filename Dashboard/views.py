from django.shortcuts import render
from Dashboard.forms import User_Form, Student_Profile_Form, Notes_Form, Search_Form, Homework_Form, Todo_Form

from Dashboard.models import Student_Profile, Notes, Homework, Todo

from django.views import generic

from django.contrib import messages

from django.shortcuts import redirect

from youtubesearchpython import VideosSearch

import requests

import wikipedia as wiki

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, 'Dashboard/index.html', context={})

def invalidPage(request):
    return render(request,"Dashboard/invalidPage.html")

@login_required
def validPage(request):
    return render(request,"Dashboard/validPage.html")

@login_required
def logout(request):
    return render(request,"Dashboard/index.html")

def signup(request):
    registered = False

    if request.method == "POST":
        userForm = User_Form(data=request.POST)
        profileForm = Student_Profile_Form(data=request.POST)

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            profile = profileForm.save(commit=False)
            profile.user = user

            if 'Student_Profile_Photo' in request.FILES:
                profile.Student_Profile_Photo = request.FILES['Student_Profile_Photo']

            profile.save()

            registered = True

        else:
            print(userForm.errors, profileForm.errors)

    else:
        userForm = User_Form()
        profileForm = Student_Profile_Form()

    Sign_Up_Dict = {"userForm": userForm,
                    "profileForm": profileForm, "registered": registered}
    return render(request, "Dashboard/signup.html", Sign_Up_Dict)


def signin(request):
    User_Name = request.user.username
    tried = False
    authenticated = False
    if request.method == "POST":
        userName = request.POST.get("userName")
        userPassword = request.POST.get("userPassword")

        user = authenticate(username=userName,password=userPassword)

        if user:
            tried = True
            authenticated = True
            if user.is_active:
                login(request, user)
                #return render(request,"Dashboard/user_index.html",{'tried':tried,'authenticated':authenticated,"User_Name":User_Name,})
                return redirect("Dashboard:user_index")

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE...")

        else:
            tried = True
            authenticated = False
            print("LOGIN FAILED...\nTRY AGAIN...")
            print(f"USERNAME(={userName}) OR PASSWORD(={userPassword}) ENTERED ARE INVALID!!")
            return render(request,"Dashboard/signin.html",{'tried':tried,'authenticated':authenticated,"User_Name":User_Name,})
    else:
        return render(request,"Dashboard/signin.html",{'tried':tried,'authenticated':authenticated,"User_Name":User_Name,})



# USER FUNCTIONS
# @login_required
def user_index(request):
    User_Name = request.user.username
    User_Index_Dict = {
        "User_Name" : User_Name,
    }
    return render(request, 'Dashboard/user_index.html', context=User_Index_Dict)

# @login_required
def notes(request):
    if request.method == 'POST':
        notesForm = Notes_Form(data=request.POST)
        if notesForm.is_valid():
            notes = Notes(user=request.user,Note_Title=request.POST['Note_Title'],Note_Description=request.POST['Note_Description'],Note_Document=request.POST['Note_Document'])
            notes.save()
        messages.success(request,f"Note Added Successfully By {request.user.username}!!")
    else:
        notesForm = Notes_Form()
    notes = Notes.objects.filter(user=request.user)
    Notes_Dict = {
        "notes" : notes,
        "notesForm" : notesForm,
        "username" : request.user.username,
    }
    return render(request, 'Dashboard/notes.html', context=Notes_Dict)

# @login_required
def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(request,f"Note Deleted Successfully By {request.user.username}!!")
    return redirect("Dashboard:notes")

class NotesDetailView(generic.DetailView):
    model = Notes

# @login_required
def youtube(request):
    if request.method == 'POST':
        searchForm = Search_Form(request.POST)
        Search_Text = request.POST['Search_Text']
        videos = VideosSearch (Search_Text,limit=18)
        Search_Result_List = []
        for video in videos.result()['result']:
            Search_Result_Dict = {
                "searchText" : Search_Text,
                "videoTitle" : video["title"],
                "videoDuration" : video["duration"],
                "videoThumbnail" : video["thumbnails"][0]['url'],
                "videoChannel" : video["channel"]["name"],
                "videoLink" : video["link"],
                "videoViewCount" : video["viewCount"]["short"],
                "videoPublishedTime" : video["publishedTime"],
            }
            description = ""
            if video["descriptionSnippet"]:
                for line in video["descriptionSnippet"]:
                    description += line["text"]
            Search_Result_Dict["videoDescription"] = description
            Search_Result_List.append(Search_Result_Dict)
            Youtube_Dict = {
                "searchForm" : searchForm,
                "Search_Result" : Search_Result_List,
            }
        return render(request,'Dashboard/youtube.html',context=Youtube_Dict)
    else:
        searchForm = Search_Form()
    Youtube_Dict = {
        "searchForm" : searchForm,
    }
    return render(request,'Dashboard/youtube.html',context=Youtube_Dict)

# @login_required
def wikipedia(request):
    if request.method == 'POST':
        searchForm = Search_Form(request.POST)
        Search_Text = request.POST['Search_Text']
        Search_Result_Wikipedia = wiki.page(Search_Text)
        Wikipedia_Dict = {
            "searchForm" : searchForm,
            "wikipediaTitle" : Search_Result_Wikipedia.title,
            "wikipediaURL" : Search_Result_Wikipedia.url,
            "wikipediaSummary" : Search_Result_Wikipedia.summary,
        }
        return render(request,'Dashboard/wikipedia.html',context=Wikipedia_Dict)
    else:
        searchForm = Search_Form()
        Wikipedia_Dict = {
            "searchForm" : searchForm,
        }
    return render(request,'Dashboard/wikipedia.html',context=Wikipedia_Dict)




# @login_required
def homework(request):
    if request.method == "POST":
        homework_form = Homework_Form(request.POST)
        if homework_form.is_valid():
            try:
                finished = request.POST["Homework_Finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                Homework_Subject = request.POST["Homework_Subject"],
                Homework_Title = request.POST["Homework_Title"],
                Homework_Description = request.POST["Homework_Description"],
                Homework_Due = request.POST["Homework_Due"],
                Homework_Finished = finished
            )
            homeworks.save()
            messages.success(request,f"Homework added from {request.user.username}.")
    else:
        homework_form = Homework_Form()
    homework = Homework.objects.filter(user = request.user)
    if len(homework) == 0:
        homework_done =  True
    else:
        homework_done = False
    context = {'homeworks':homework,'homeworks_done':homework_done,'homework_form':homework_form, 'username': request.user.username}
    return render(request,'Dashboard/homework.html',context)


# @login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.Homework_Finished == True:
        homework.Homework_Finished = False
    else:
        homework.Homework_Finished = True
    homework.save()
    return redirect('Dashboard:homework')

# @login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    messages.success(request,f"Homework Deleted Successfully By {request.user.username}!!")
    return redirect('Dashboard:homework')

# @login_required
def books(request):
    if request.method == "POST":
        searchForm = Search_Form()
        Search_Text = request.POST['Search_Text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+Search_Text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('Categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)

            Books_Dict = {
                "searchForm" : searchForm,
                'results' : result_list,
            }
        return render(request,"Dashboard/books.html", context = Books_Dict)
    else:
        searchForm = Search_Form()
    Books_Dict = {
        'searchForm':searchForm,
    }
    return render(request,"Dashboard/books.html", context = Books_Dict)


# @login_required
def todo(request):
    if request.method == 'POST':
        form = Todo_Form(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["Todo_Finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                Todo_User = request.user,
                Todo_Title = request.POST['Todo_Title'],
                Todo_Finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added Successfully.")
    else:
        form = Todo_Form()
    todo = Todo.objects.filter(Todo_User=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False

    Todo_dict = {
        'username' : request.user.username,
        'form' : form,
        'todos' : todo,
        'todos_done' : todos_done,
    }
    return render(request,"Dashboard/todo.html",Todo_dict)


# @login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.Todo_Finished == True:
        todo.Todo_Finished = False
    else:
        todo.Todo_Finished = True
    todo.save()
    return redirect('Dashboard:todo')


# @login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    messages.success(request,f"Todo Deleted Successfully.")
    return redirect("Dashboard:todo")

# @login_required
def dictionary(request):
    if request.method == 'POST':
        form = Search_Form(request.POST)
        Search_Text = request.POST['Search_Text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+Search_Text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            Dictionary_Dict = {
                'form':form,
                'input':Search_Text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
            }
        except:
            Dictionary_Dict = {
                'form':form,
                'input':'',
            }
        return render(request,'Dashboard/dictionary.html',Dictionary_Dict)
    else:
        form = Search_Form()
        Dictionary_Dict = {
        'form':form,
        }
    return render(request,'Dashboard/dictionary.html',Dictionary_Dict)

# @login_required
def profile(request):
    User_Name = request.user.username
    Homework_List = Homework.objects.filter(Homework_Finished=False, user=request.user)
    Todo_List = Todo.objects.filter(Todo_Finished=False, Todo_User=request.user)
    if len(Homework_List) == 0:
        Homework_Done = True
    else:
        Homework_Done = False
    if len(Todo_List) == 0:
        Todo_Done = True
    else:
        Todo_Done = False
    Due_Dict = {
        "User_Name" : User_Name,
        "Homework_List" : Homework_List,
        "Todo_List" : Todo_List,
        "Homework_Done" : Homework_Done,
        "Todo_Done" : Todo_Done,
    }
    return render(request,'Dashboard/profile.html',context=Due_Dict)
