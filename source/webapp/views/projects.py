from django.urls import reverse
from django.views.generic import ListView, CreateView

from webapp.forms import ProjectForm
from webapp.models import Project, Task


class ProjectsView(ListView):
    template_name = 'project/projects.html'

    context_object_name = 'projects'
    model = Project
    ordering = ['started_at']


class ProjectDetailView(ListView):
    template_name = 'project/project_detail.html'

    context_object_name = 'tasks'
    model = Task


    def get_queryset(self):
        self.project = Project.objects.get(pk=self.kwargs['pk'])
        queryset = super().get_queryset()
        return queryset.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class ProjectCreateView(CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})
