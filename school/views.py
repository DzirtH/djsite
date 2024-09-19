import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddPostForm, RegisterUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .utils import *

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'school/logo_register.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    return render(request, 'school/logo_register.html', {'form': form})


class SchoolHome(DataMixin, ListView):
    paginate_by = 3
    model = Catalog
    template_name = 'school/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Catalog.objects.filter(is_published=True)


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'school/home_old.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    context = {'room': room, 'room_messages': room_messages, }
    return render(request, 'school/room.html', context)


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Catalog.objects.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    )
    years = Category.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
    }
    return render(request, 'school/index.html', context=context)


# Добавления любого класса или функцию пример добавить книгу это делается когда автаризован тогда испрользовут эту функцию
@login_required(login_url='/login')
def about(request):
    contact_list = Catalog.objects.all()
    return render(request, 'school/about.html', {'menu': menu, 'title': 'О сайте'})


class Addpage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'school/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


@login_required(login_url='/login')
def addpage(request):

    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request, 'school/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление издания'})


def contact(request):
    return HttpResponse("Обратная связь")


def loginA(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Catalog
    template_name = 'school/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


@login_required(login_url='/login')
def show_post(request, post_slug):
    post = Catalog.objects.get(id=post_slug)

    # if request.user != post.title:
    #     return HttpResponse('Your are not allowed here!!')
    # messages = post.message_set.all()
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'year_selected': 1,
        # 'messages': messages,
    }
    return render(request, 'school/post.html', context)


class SchoolCategory(ListView):
    model = Catalog
    template_name = 'school/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self().get_user_context(title='Категории -' +
                                        str(context['posts'][0].year), year_selected=context['post'][0].year_id)
        return context

    def get_queryset(self):
        return Catalog.objects.filter(year__slug=self.kwargs['year_slug'], is_published=True)


def show_category(request, year_slug):
    posts = Catalog.objects.filter(year_id=year_slug)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Издания',
        'year_selected': year_slug,
    }
    return render(request, 'school/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'school/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
