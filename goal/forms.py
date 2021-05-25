from django import forms
from goal.models import Goal, User, Comment
from django.contrib.auth.forms import UserCreationForm


class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'publicity', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 65,
                'rows': 5,
                'placeholder': '(optional)'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', ]
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 65,
                'rows': 2,
                'placeholder': '(optional)'
            })
        }


class SignUpForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 60,
        'rows': 6,
        'placeholder': 'Let the world know about you and your goals',
    }),
        required=False, help_text='(Optional)')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'bio')


# class Comment(models.Model):
#     owner = models.ForeignKey(User,
#                               on_delete=models.CASCADE)
#     title = models.CharField(max_length=150)
#     text = models.TextField(
#         validators=[MinLengthValidator(
#             3, "Comment must be greater than 3 characters")]
#     )
#     goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
#     posted_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.title}, on goal: {self.goal}"

#     def get_absolute_url(self):
#         return self.goal.get_absolute_url()
