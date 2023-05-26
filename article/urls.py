from django.urls import path
from . import views

urlpatterns = [
    path("<int:article_id>/comments/", views.CommentsView.as_view()),  # 특정 게시글에 코멘트 작성.
    path("<int:article_id>/comments/<comment_id>/", views.DetailComments.as_view()),  # 특정 코멘트 수정, 삭제
    path("", views.ArticlesView.as_view()),  # 게시글 작성
    path("<int:article_id>/", views.ArticleDetailView.as_view()),  # 게시글 수정 삭제
    path("likes/<int:article_id>/", views.LikeView.as_view()),  # 좋아요 기능. 현재 Article모델이 없어서 주석처리
    path("search/", views.ArticlesSearchView.as_view(), name="search")
]

