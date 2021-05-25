from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from .models import Goal, Category, Comment, User
from .forms import CreateGoalForm, SignUpForm, CommentForm

# from django.contrib.auth.models import User


class Home(View):
    def get(self, request):
        goal_likeable = []
        goals = Goal.objects.filter(publicity='p').order_by('-upvotes')

        if request.user.is_authenticated:
            for goal in goals:
                already_liked = False
                if request.user.rated_goals.filter(id=goal.id).exists():
                    already_liked = True
                goal_likeable += [{
                    'goal': goal,
                    'already_liked': already_liked,
                }]
        else:
            goal_likeable = [{'goal': goal, 'already_liked': False}
                             for goal in goals]

        paginator = Paginator(goal_likeable, 10)
        page_number = request.GET.get('page')
        # assign this to goal_likeable so that
        goal_likeable_paginated = paginator.get_page(page_number)
        ctx = {
            'goal_likeable': goal_likeable_paginated,
        }
        return render(request, 'goal/index.html', context=ctx)


class CreateUser(View):
    def get(self, request):
        form = SignUpForm()
        ctx = {'form': form}
        return render(request, 'registration/signup.html', ctx)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # if we made a valid user, save them first
            form.save()
            # then, login to the account
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('goal:user-detail', user.username_slug)

        ctx = {'form': form}
        return render(request, 'registration/signup.html', ctx)


class UserDetail(View):
    def get(self, request, username_slug):
        page_owner = get_object_or_404(User, username_slug=username_slug)
        pk = page_owner.id

        public_goals = Goal.objects.filter(owner=pk, publicity='p')
        private_goals = Goal.objects.filter(owner=pk, publicity='pr')

        public_goal_likeable = []
        for goal in public_goals:
            if goal.user_set.filter(id=request.user.id).exists():
                already_liked = True
            else:
                already_liked = False
            print(goal.created_at < goal.updated_at)

            public_goal_likeable += [{
                'goal': goal,
                'already_liked': already_liked,
            }]

        private_goal_likeable = []
        # we defined manytomany field in User as rated_goals
        # we can access a user's rated goals with user_object.rated_goals.all()

        # we can access the users that rated a goal with goal_object.user_set.all()

        for goal in private_goals:
            if goal.user_set.filter(id=request.user.id).exists():
                already_liked = True
            else:  # TODO: THIS ALWAYS GIVES FALSE AND THAT NEEDS TO CHANGE
                already_liked = False

            private_goal_likeable += [{
                'goal': goal,
                'already_liked': already_liked,
            }]

        # print(public_goal_likeable)
        ctx = {
            'page_owner': page_owner,
            # don't really need these two anymore
            'public_goals': public_goals,
            'private_goals': private_goals,

            'public_goal_likeable': public_goal_likeable,
            'private_goal_likeable': private_goal_likeable,
        }
        print(private_goal_likeable)

        return render(request, 'goal/user_detail.html', context=ctx)


class LikeGoal(View, LoginRequiredMixin):
    def post(self, request, id):
        user = User.objects.get(id=request.user.id)
        goal = Goal.objects.get(id=id)

        if Goal.objects.filter(id=id, user=request.user).exists():
            user.rated_goals.remove(goal)
            goal.upvotes = goal.upvotes - 1
        else:
            user.rated_goals.add(goal)
            goal.upvotes = goal.upvotes + 1

        goal.save()

        next = request.POST.get('next', '/')
        return redirect(next)


class CreateGoalView(View, LoginRequiredMixin):
    template_name = 'goal/goal_form.html'

    def get(self, request):
        form = CreateGoalForm()
        ctx = {
            'form': form,
            'type': 'create',
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        success_url = reverse(
            'goal:user-detail', args=[self.request.user.username_slug])

        form = CreateGoalForm(request.POST)

        if not form.is_valid():
            ctx = {
                'form': form,
                'type': 'create',
            }
            return render(request, self.template_name, ctx)
        # if is valid:
        goal = form.save(commit=False)
        goal.owner = self.request.user
        goal.upvotes = 0
        goal.save()
        return redirect(success_url)


class GoalUpdateView(LoginRequiredMixin, View):
    template_name = 'goal/goal_form.html'

    def get(self, request, username_slug, pk, goal_slug):
        goal = get_object_or_404(
            Goal,
            id=pk,
            owner__username_slug=self.request.user.username_slug,
            goal_slug=goal_slug
        )
        form = CreateGoalForm(instance=goal)

        ctx = {
            'form': form,
            'type': 'update',
        }
        return render(request, self.template_name, ctx)

    def post(self, request, username_slug, pk, goal_slug):
        success_url = request.GET.get('next')
        if not success_url:
            success_url = reverse_lazy(
                'goal:user-detail', args=[request.user.username_slug])

        goal = get_object_or_404(Goal, id=pk, owner=self.request.user)
        form = CreateGoalForm(request.POST, instance=goal)

        if not form.is_valid():
            ctx = {
                'form': form,
                'type': 'update',
            }
            return render(request, self.template_name, ctx)

        goal = form.save(commit=False)
        goal.save()

        return redirect(success_url)


class GoalDetail(View):
    def get(self, request, username_slug, pk, goal_slug, comment_form=None):
        page_owner = get_object_or_404(User, username_slug=username_slug)
        goal = Goal.objects.get(
            owner__username_slug=username_slug,
            pk=pk,
            goal_slug=goal_slug,
        )

        if goal.publicity == 'pr' and page_owner != request.user:
            return HttpResponse(status=403)

        print(comment_form, "inside GoalDetail")
        if not comment_form:
            comment_form = CommentForm()
        comments = goal.comment_set.all()

        already_liked = False
        if request.user.is_authenticated and request.user.rated_goals.filter(id=goal.id).exists():
            already_liked = True
        ctx = {
            'page_owner': page_owner,
            'goal': goal,
            'already_liked': already_liked,
            'comment_form': comment_form,
            'comments': comments,
        }

        return render(request, 'goal/goal_detail.html', context=ctx)


class GoalDelete(View, LoginRequiredMixin):
    def post(self, request, id):
        goal = Goal.objects.get(id=id)
        creator = goal.owner
        if creator != request.user:
            return HttpResponse(status=403)

        goal.delete()
        return redirect('goal:user-detail', creator.username_slug)


class CreateComment(View, LoginRequiredMixin):
    def post(self, request, id):
        # pass in the goal's id, then redirect to this
        # add the post to the one-to-many field for the comments
        goal = Goal.objects.get(id=id)
        success_url = reverse(
            'goal:goal-detail', kwargs={
                'username_slug': goal.owner.username_slug,
                'pk': id,
                'goal_slug': goal.goal_slug
            }
        )

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.goal = goal
            comment.save()
        print(form, "inside CreateComment")
        return redirect(success_url, comment_form=form)


class DeleteComment(View, LoginRequiredMixin):
    def post(self, request, id):
        if Comment.objects.filter(id=id, owner=request.user).exists():
            comment = Comment.objects.get(id=id)
            goal = comment.goal
            comment.delete()

            success_url = reverse('goal:goal-detail', kwargs={
                'username_slug': goal.owner.username_slug,
                'pk': goal.id,
                'goal_slug': goal.goal_slug,
            })

            return redirect(success_url)
        return HttpResponse(status=403)


class Categories(View):
    def get(self, request):
        return HttpResponse("This will show all the top categories")


class CategoryDetail(View):
    def get(self, request, category_slug):
        return HttpResponse("This shows details about a category")


# class UserDetail2(View):
#     def get(self, request, pk):
#         page_owner = get_object_or_404(User, id=pk)
#         public_goals = Goal.objects.filter(owner=pk, publicity='p')
#         private_goals = Goal.objects.filter(owner=pk, publicity='pr')

#         user = request.user
#         likeable = []

#         for goal in public_goals:
#             if Goal.objects.filter(user__id=request.user.id).exists():
#                 already_liked = True
#             else:
#                 already_liked = False

#             likeable += [(goal, already_liked)]

#         print(likeable)
#         ctx = {
#             'public_goals': public_goals,
#             'likeable': likeable,
#         }
#         return render(request, 'goal/2_user_detail.html', ctx)
