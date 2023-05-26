from rest_framework.views import APIView
from . models import Articles,Comments
from . serializer import CommentCreateSerializer, ArticleCreateSerializer, ArticleListSerializer, CommentSerializer,ArticleSerializer, ArticleSearchSerializer
from rest_framework.response import Response
from rest_framework import status, filters, generics
from rest_framework.generics import get_object_or_404
from PIL import Image


# Create your views here.

class ArticlesView(APIView):
    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        articles = Articles.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user == article.author:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다.', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        if request.user == article.author:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)

class CommentsView(APIView):
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, article_id):
        article = Articles.objects.get(id = article_id)
        comments = article.comment.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class DetailComments(APIView):
    def patch(self, request, comment_id, article_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comments ,id = comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없다.', status=status.HTTP_403_FORBIDDEN)
        
class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        serializer = ArticleListSerializer(article)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"result": "unlike", "count":len(serializer.data['likes'])}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"result": "like", "count":len(serializer.data['likes'])}, status=status.HTTP_200_OK)


class ArticlesSearchView(generics.ListCreateAPIView):
    search_fields = ["title", "content", "author__email"]
    filter_backends = (filters.SearchFilter,)
    
    queryset = Articles.objects.all()
    serializer_class = ArticleListSerializer