from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework import permissions,status, generics,viewsets
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from guru.serializers import *
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.db.models import Q


cloudinary.config(
  cloud_name = "guruapp",
  api_key = "328295839766139",
  api_secret = "fw8b85Ig7I0e2bOslPzvRjjaCHM"
)


class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.values('avi__avi_path','id','username','type').all()
    serializer_class = FilterSerializer


class RegistrationView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        aboutUser = AboutUser.objects.create(user_id=user)
        aboutUser.save()
        default ='https://res.cloudinary.com/guruapp/image/upload/c_scale,h_287,w_249/v1558568880/profile-blank_dzejyo.png'
        avi = Avi.objects.create(user_id=user.id, avi_path=default)
        avi.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get_or_create(user= user)[0].key,
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get_or_create(user=user)[0].key,

        })

class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()

        except (AttributeError, ObjectDoesNotExist):
            return Response({"fail":("Failed logged out.")},status=status.HTTP_400_BAD_REQUEST)

        return Response({"success":("Successfully logged out.")},status=status.HTTP_204_NO_CONTENT)

class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AboutUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AboutUserSerializer

    def put(self, request, *args, **kwargs):
        print(self.request.data)
        AboutUser.objects.filter(user_id=self.request.user.id).update(github=self.request.data['github'],location=self.request.data['location'],
        linkedin=self.request.data['linkedin'],twitter_handle=self.request.data['twitter_handle'],bio=self.request.data['bio'])
        return Response({"aboutUser": "updated" })




class AviView(generics.GenericAPIView):
    serializer_class = AviSerializer

    def get(self,request, **kwargs):
        avi = Avi.objects.get(user_id=int(self.kwargs['id']))
        serializer = AviSerializer(avi)
        return Response(serializer.data)

    def post(self,request, **kwargs):
        result = cloudinary.uploader.destroy(str(self.request.data['user_id']))
        return Response({"response":("result")})

    def put(self, request, *args, **kwargs):
        avi = Avi.objects.filter(user_id=int(self.request.data['user_id'])).update(avi_path = self.request.data['avi_path'],)
        return Response({"success":("Successfully submitted.")})

class WorkView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        work = serializer.save()
        return Response(WorkSerializer(work, context=self.get_serializer_context()).data)

    def delete(self,request, *args, **kwargs):
        work_id = self.kwargs['id']
        work = Work.objects.filter(id=work_id).delete()
        return Response({"success":("Successfully deleted.")})


class UserSkillsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        skill = serializer.save()
        return Response(UserSkillsSerializer(skill, context=self.get_serializer_context()).data)

    def delete(self,request, *args, **kwargs):
        skill_id = self.kwargs['id']
        skill = UserSkills.objects.filter(id=skill_id).delete()
        return Response({"id":skill_id})


class UserInterestsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = UserInterests.objects.all()
    serializer_class = UserInterestsSerializer


    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        interest = serializer.save()
        return Response(UserInterestsSerializer(interest, context=self.get_serializer_context()).data)

    def delete(self,request, *args, **kwargs):
        interest_id = self.kwargs['id']
        skill = UserInterests.objects.filter(id=interest_id).delete()
        return Response({"success":("Successfully deleted.")})


class EducationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        edu = serializer.save()
        return Response(EducationSerializer(edu, context=self.get_serializer_context()).data)

    def delete(self,request, *args, **kwargs):
        edu_id = self.kwargs['id']
        edu = Education.objects.filter(id=edu_id).delete()
        return Response({"success":("Successfully deleted.")})

# READ ONLY VIEWS
class ReadInterestsView(generics.RetrieveAPIView):
    serializer_class = UserInterestsSerializer
    queryset = UserInterests.objects.all()
    def get(self, request, username):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(None)

        interests = UserInterests.objects.filter(user_id=user.id).all()
        serializer = UserInterestsSerializer(interests,many=True)
        return Response(serializer.data)

class ReadSkillsView(generics.RetrieveAPIView):
    serializer_class = UserSkillsSerializer
    queryset = UserSkills.objects.all()
    def get(self, request, username):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(None)

        skills = UserSkills.objects.filter(user_id=user.id).all()
        serializer = UserSkillsSerializer(skills,many=True)
        return Response(serializer.data)


class ReadWorkView(generics.RetrieveAPIView):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()
    def get(self, request, username):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(None)

        work = Work.objects.filter(user_id=user.id).all().order_by('end').reverse()
        serializer = WorkSerializer(work,many=True)
        return Response(serializer.data)


class ReadEducationView(generics.RetrieveAPIView):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    def get(self, request, username):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(None)

        edu = Education.objects.filter(user_id=user.id).all().order_by('end').reverse()
        serializer = EducationSerializer(edu,many=True)
        return Response(serializer.data)

class ReadAboutUserView(generics.RetrieveAPIView):
    serializer_class = AboutUserSerializer
    def get_object(self):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        about_user = AboutUser.objects.get(user_id=user.id)

        return about_user

class ReadUserView(generics.GenericAPIView):
    serializer_class = UserViewSerializer
    queryset = User.objects.all()
    def get(self,request,**kwargs):
        try:
            username = str(self.kwargs['username'])
            user = User.objects.filter(username=username).values('avi__avi_path','id','type','username',
            'first_name','last_name')
            user_ser = UserViewSerializer(user,many=True)
            return Response(user_ser.data)
        except User.DoesNotExist:
            user = None
        return user

#SEARCH
class FilterUserView(generics.GenericAPIView):
    serializer_class = FilterSerializer
    queryset = User.objects.all()
    def post(self,request,**kwargs):
        query = self.request.data['query'].strip()

        school = User.objects.filter(education__school__icontains=query).values('avi__avi_path','id','username',
        'type').distinct()
        company = User.objects.filter(work__company__icontains=query).values('avi__avi_path','id','username',
        'type').distinct()
        location = User.objects.filter(aboutuser__location__icontains=query).values('avi__avi_path','id','username',
        'type').distinct()
        skill = User.objects.filter(userskills__skill__icontains=query).values('avi__avi_path','id','username',
        'type').distinct()
        interest = User.objects.filter(userinterests__interest__icontains=query).values('avi__avi_path','id','username',
        'type').distinct()
        name = User.objects.filter(Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query)).values('avi__avi_path','id',
        'username','type').distinct()

        all = User.objects.filter(Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query)
        |Q(education__school__icontains=query)|Q(work__company__icontains=query)|Q(aboutuser__location__icontains=query)|
        Q(userskills__skill__icontains=query)|Q(userinterests__interest__icontains=query)).values('avi__avi_path','id','username'
        ,'type').distinct()

        school_ser = FilterSerializer(school,many=True)
        company_ser = FilterSerializer(company,many=True)
        location_ser = FilterSerializer(location,many=True)
        skill_ser = FilterSerializer(skill,many=True)
        interest_ser = FilterSerializer(interest,many=True)
        name_ser = FilterSerializer(name,many=True)
        all_ser = FilterSerializer(all,many=True)

        return Response({"school":school_ser.data,"company":company_ser.data,"location":location_ser.data,
        "skill":skill_ser.data,"interest":interest_ser.data,"name":name_ser.data,"all":all_ser.data})


class CategoryView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(CategorySerializer(category, context=self.get_serializer_context()).data)

    def get(self,request):
        categories = Category.objects.all().order_by('name')
        cat_ser = CategorySerializer(categories,many=True)
        data = cat_ser.data

        for x in data:
            x['topics']=Topic.objects.filter(category=x['id']).count()
            x['posts']=Post.objects.filter(category=x['id']).count()

        return Response(data)

class TopicView(generics.GenericAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.save()
        return Response(TopicSerializer(topic, context=self.get_serializer_context()).data)

    def get(self,request,**kwargs): #get all topics of category
        id = self.kwargs['cat_id']
        topics = Topic.objects.filter(category=id)
        category = Category.objects.get(id=id).name
        topic_ser = TopicSerializer(topics,many=True)
        data = topic_ser.data
        for x in data:
            x['posts']=Post.objects.filter(topic=x['id']).count()
        return Response({'data':data,'category':category})



class PostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post, context=self.get_serializer_context()).data)

    def get(self,request,**kwargs):

        def getChildren(id):
            posts = Post.objects.filter(reply_to_id=id).reverse()
            post_ser = PostSerializer(posts,many=True)
            post_ser = PostSerializer(posts,many=True)
            data = post_ser.data
            return data

        def comments_to_dicts(comments):
            results = []  # create list for results
            for comment in comments:  # iterate over comments
                item = {
                    "id": comment['id'],
                    "text": comment['text'],
                    "reply_to":comment['reply_to'],
                    "user_id":comment['user_id']
                }  # create dict from comment
                replies = getChildren(comment['id'])
                if len(replies) > 0:
                    item["replies"] = comments_to_dicts(replies)  # convert replies using the same function
                results.append(item)  # add converted item to results
            return results  # return all converted comments
        id = self.kwargs['top_id']
        posts = Post.objects.filter(topic=id,reply_to__isnull=True).order_by('id').reverse()
        topic = Topic.objects.get(id=id).name
        post_ser = PostSerializer(posts,many=True)
        data = post_ser.data

        meta={}
        user_ids = Post.objects.filter(topic=id).values('user_id').distinct()
        for x in user_ids:
            id = x['user_id']
            meta[id]={}
            meta[id]['avi_path']= Avi.objects.filter(user_id=id).values('avi_path')[0]['avi_path']
            meta[id]['username']= User.objects.filter(id=id).values('username')[0]['username']

        user_avi = User.objects.filter(id=self.request.user.id).values('avi__avi_path')[0]['avi__avi_path']
        data=comments_to_dicts(data)
        return Response({'data':data,'topic':topic,'meta':meta,'user_avi':user_avi})

    def delete(self,request,**kwargs):
        id = self.request.data['id']
        assert (self.request.user.id == Post.objects.filter(id=id).values('user_id')[0]['user_id'])
        post = Post.objects.filter(id=id).delete()
        return Response({"Post deleted"})

from django.http import HttpResponse

class RecentTopicView(generics.GenericAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get(self,request,**kwargs):
        topics = Topic.objects.all().order_by('-id')[:10]
        serializer = TopicSerializer(topics,many=True)
        return Response(serializer.data)



class UserTopicView(generics.GenericAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self,request,**kwargs):
        topics = Topic.objects.filter(created_by=self.request.user.id)
        serializer = TopicSerializer(topics,many=True)
        return Response(serializer.data)

    def delete(self,request,**kwargs):
        id = self.request.data['id']
        assert (self.request.user.id == Topic.objects.filter(id=id).values('created_by')[0]['created_by'])
        topic = Topic.objects.filter(id=id).delete()
        return Response({"Topic deleted"})
