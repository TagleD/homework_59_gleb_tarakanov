from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from webapp.forms import TaskForm, SimpleSearchForm
from webapp.models import Task


class TasksView(ListView):
    template_name = 'task/tasks.html'

    context_object_name = 'tasks'
    model = Task
    ordering = ['created_at']

    paginate_by = 9
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            # Сделал по title и description, так как в этом проекте title выполняет
            # функцию краткого описания
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset


    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TaskDetailView(DetailView):
    template_name = 'task/task_detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = self.object.type.all()
        return context

class TaskAddView(CreateView):
    template_name = 'task/add_task.html'
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    template_name = 'task/update_task.html'
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk': self.object.pk})

class DeleteView(TemplateView):
    template_name = 'task/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class ConfirmDelete(View):

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect('index')
