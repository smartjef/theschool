from django import forms
from .models import Lesson, Comment, Reply

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        #fields = ('__all__')
        fields = ('lesson_id', 'name', 'position','description','d_notes','code','image', 'video', 'ppt', 'Notes')
        #exclude = ('subject', 'created_by', 'created_at')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body":"Comment"}

        widgets={
            'body': forms.Textarea(attrs={'class':'form-control', 'rows': 4, 'cols': 60, 'placeholder': "Enter your comment..."})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm,self).__init__(*args, **kwargs)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)
        widgets = {'reply_body' : forms.Textarea(attrs={'class':'form-control', 'rows':2, 'cols': 30, 'placeholder':"Add an reply..."}),}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm,self).__init__(*args, **kwargs)