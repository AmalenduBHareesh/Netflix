from django.shortcuts import render
from app.models import*
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


#user-signup

def signup(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('app:signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('app:signup')

            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('app:userlogin')   

        else:
            messages.info(request,'Password is Not Matching')    
            return redirect('app:signup')

    return render(request,'signup.html')  
    


# user-login   

def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('app:index')
        else:
            messages.info(request,'Credentials invalid!')
            return redirect('app:userlogin')
    return render (request,'login.html')



#index-view



@login_required
def index(request):
    movies = Movie.objects.all()
    genre = Genre.objects.all()

    context = {
        'movies': movies,
        'genre': genre,
        'movie_genre': 'All',  # default title
    }

    return render(request, 'index.html', context)


def userlogout(request):
    auth.logout(request)
    return redirect('app:userlogin')


@login_required
def genre_view(request, id):
    # Search by 'name' because 'id' is now the string "Animation"
    genre_obj = Genre.objects.get(name=id) 
    movies = Movie.objects.filter(genre=genre_obj)

    context = {
        'movies': movies,
        'genre': Genre.objects.all(),
        'movie_genre': genre_obj.name,
    }

    return render(request, 'index.html', context)



@login_required
def my_list(request):
    my_movies = Movielist.objects.filter(owner_user=request.user)
    genre = Genre.objects.all()

    context = {
        'movies': [m.movie for m in my_movies],
        'genre': genre,
        'movie_genre': "My List",
    }

    return render(request, 'index.html', context)


@login_required
def search(request):
    if request.method == "POST":
        term = request.POST.get('search_term')

        movies = Movie.objects.filter(title__icontains=term)
        genre = Genre.objects.all()

        context = {
            'movies': movies,
            'genre': genre,
            'movie_genre': f"Search: {term}",
        }

        return render(request, 'index.html', context)

    return redirect('app:index')




@login_required
def add_to_list(request):
    if request.method == "POST":
        movie_id = request.POST.get('movie_id')

        try:
            movie = Movie.objects.get(uu_id=movie_id.split('/')[-1])
            Movielist.objects.create(
                owner_user=request.user,
                movie=movie
            )
            return JsonResponse({'message': 'Added ✅'})
        except:
            return JsonResponse({'message': 'Error ❌'})

    return JsonResponse({'message': 'Invalid request'})