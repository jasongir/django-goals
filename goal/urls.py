
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'goal'

urlpatterns = [
    # shows the public highest-upvoted lists
    path('', views.Home.as_view(), name='home'),

    path('signup/', views.CreateUser.as_view(), name='signup'),

    # shows the user's public lists, and private lists if logged in
    path('u/<slug:username_slug>/', views.UserDetail.as_view(), name='user-detail'),

    # shows edit/delete for lists, or view only if someone else's
    path('u/<slug:username_slug>/<int:pk>/<slug:goal_slug>/',
         views.GoalDetail.as_view(), name='goal-detail'),

    # comment on a goal, pass in the goal's id
    path('comment/<int:id>/', views.CreateComment.as_view(), name='create-comment'),
    # delete a comment, pass in the comment's id
    path('comment-delete/<int:id>/',
         views.DeleteComment.as_view(), name='delete-comment'),


    # update view
    path('u/<slug:username_slug>/<int:pk>/<slug:goal_slug>/update/',
         views.GoalUpdateView.as_view(), name='goal-update'),

    # delete view
    path('goal-delete/<int:id>/', views.GoalDelete.as_view(), name='goal-delete'),

    # # shows the top 10 most upvoted items in this category
    # path('category/<slug:category_slug>/',
    #      views.CategoryDetail.as_view(), name='category'),
    # # shows all of the top categories
    # path('category/', views.Categories.as_view(), name='categories'),

    path('create/', views.CreateGoalView.as_view(), name='create-goal'),

    path('like-goal/<int:id>/', views.LikeGoal.as_view(), name='like-goal'),
]
