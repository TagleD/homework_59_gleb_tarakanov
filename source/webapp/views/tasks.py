from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import TaskForm
from webapp.models import Task


class TasksView(TemplateView):
    template_name = 'tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class DetailView(TemplateView):
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        context['types'] = context['task'].type.all()
        return context


class AddView(TemplateView):
    template_name = 'add_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'add_task.html', context={
                'form': form
            })
        else:
            task = form.save()
            return redirect('detail_view', pk=task.pk)


class UpdateView(TemplateView):
    template_name = 'update_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        context['form'] = TaskForm(instance=context['task'])
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('detail_view', pk=task.pk)
        return render(request, 'update_task.html', context={'form': form, 'task': task})


class DeleteView(TemplateView):
    template_name = 'confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class ConfirmDelete(View):

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect('index')
