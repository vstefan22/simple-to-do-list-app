
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from . import models

class Index(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'todo_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        
        
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains = search_input)

        context['search_input'] = search_input

        return context 

class TaskDetail(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'todo_app/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class UpdateView(LoginRequiredMixin, UpdateView):
    model = models.Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('index')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy('index')

class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterPage(FormView):
    template_name = 'todo_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

def black_white(request):
    if request.method == "GET":
        color = request.GET.get('color')
        #cnt = request.session.get('cnt_views', 0)
        #request.session['cnt_views'] = cnt+1
        clr = request.session.get('clr', 'white')
        if color == 'black':
            request.session['clr'] = 'black'
        if color == 'white':
            request.session['clr'] = 'white'
        context = {
            'color':color,
            #'cnt':cnt
            'clr':clr
        }
        
        return render (request, 'todo_app/settings.html', context)
    


