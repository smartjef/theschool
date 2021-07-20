from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LessonForm, CommentForm, ReplyForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission, User
from django.views.generic import TemplateView, DetailView, ListView,FormView, CreateView, UpdateView, DeleteView
from .models import Standard, Subject, Lesson, Comment, WorkingDays, TimeSlots
# Create your views here.
from django.db.models import Q



class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'courses/standard_list_view.html'

class SubjectListView(DetailView):
    context_object_name = 'standards'
    extra_context = {
        'slots': TimeSlots.objects.all() or WorkingDays.objects.all()
    }
    model = Standard
    template_name = 'courses/subject_list_view.html'
class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'courses/lesson_list_view.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        print(context.get("object"))
        # context[""]
        return context

class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'courses/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)

        if 'form2' not in context:
            context['form2'] = self.second_form_class(request= self.request)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.form_class
            form_name = 'form'

        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print("comment form if returned")
            return self.form_valid(form)

        elif form_name == 'form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('lesson_detail', kwargs={'standard': standard.slug, 'subject':subject.slug, 'slug':self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm =form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm =form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'courses/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('lesson_list',kwargs={'standard':standard.slug, 'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
class LessonUpdateView(UpdateView):
    fields = ('name','position','description','d_notes','code','image','video','ppt','Notes')
    model = Lesson
    template_name = 'courses/lesson_update.html'
    context_object_name = 'lessons'

class LessonDeleteView(DeleteView):

    model = Lesson
    context_object_name = 'lessons'
    template_name = 'courses/lesson_delete.html'

    def get_success_url(self):
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('lesson_list', kwargs={'standard': standard.slug,'slug':subject.slug})

def search(request):
    ans = request.GET['q']
    q = Standard.objects.filter(name__icontains=ans) or Subject.objects.filter(name__icontains=ans) or Lesson.objects.filter(name__icontains=ans)
    user = User.objects.filter(username__icontains=ans) or User.objects.filter(email__icontains=ans)
    context = {
        'ans': ans,
        'q' : q,
        'search_user' : user,
    }
    return render(request, 'search.html', context)