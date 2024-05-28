from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import RegistrationForm,ReviewForm
from django.core.paginator import  Paginator
from .models import Category,publisher, Book, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages 
# Create your views here.



def index(request):
    categories = Category.objects.all()
    newpublished = Book.objects.order_by('-created')[:15]
    return render(request, 'index.html', {'categories': categories,'newpublished':newpublished})
    
    


#-----login-------#

def signin(request):
    if request.user.is_authenticated:
        return redirect('store:index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('store:index')
         
    return render(request, "login.html")	



#-----logout-------#

def signout(request):
    logout(request)
    return redirect('store:index')	





#-----registration------#

def registration(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('store:signin')

	return render(request, 'signup.html', {"form": form})


#-------All Books------#
@login_required(login_url='store:signin')
def get_books(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        books = Book.objects.filter(category_id=category_id)
    else:
        books = Book.objects.all()
    context = {
        'categories': categories,
        'books': books,
    }
    return render(request, 'category.html', context)



#--------Get books by category-------#
@login_required(login_url='store:signin')
def get_book_category(request, id):
    categories = Category.objects.all()
    book_ = Book.objects.filter(category_id=id)
    paginator = Paginator(book_, 10)
    page = request.GET.get('page')
    book = paginator.get_page(page)
    category = get_object_or_404(Category, id=id)
    return render(request, "category.html", {"books": book, "categories": categories, "category": category})


#-------Get Book-----#

@login_required(login_url='store:signin')
def get_book(request, id):
    form = ReviewForm(request.POST or None)
    book = get_object_or_404(Book, id=id)
    rbooks = Book.objects.filter(category_id=book.category.id)
    r_review = Review.objects.filter(book_id=id).order_by('-created')
    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)
    categories = Category.objects.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.customer = User.objects.get(id=request.user.id)
                temp.book = book          
                temp = Book.objects.get(id=id)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                form.save()  
                temp.save()

                messages.success(request, "Review Added Successfully")
                form = ReviewForm()
        else:
            messages.error(request, "You need login first.")
    context = {
        "book":book,
        "rbooks": rbooks,
        "form": form,
        "rreview": rreview,
        'categories': categories,
       
    }
    return render(request, "book.html", context)


@login_required(login_url='store:signin')
def get_publisher(request, id):
    pub = get_object_or_404(publisher, id=id)
    book = Book.objects.filter(publisher_id=pub.id)
    context = {
        "wrt": pub,
        "book": book
    }
    return render(request, "store/writer.html", context)






