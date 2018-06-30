# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals

import datetime
from django.conf import settings
import stripe
from textblob import TextBlob

stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth.views import LoginView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm,Requestform
from django.contrib.auth.models import User
from .tokens import account_activation_token
from .models import Query, SocialData, Query, SocialDataQuery,Token


# Create your views here.


def home(request):
    q=Query.objects.filter(is_public=True)
    template = loader.get_template('website/index.html')
    context = {
        'name': "SMS - Social Media Survey",
        'query':q,
    }
    r = template.render(context, request)
    return HttpResponse(r)
    # instead we can use return render(request, 'website/index.html', context)
def user(request):
    user=request.user
    q=User.objects.filter(username=user)
    if q:
        q = Token.objects.filter(user_id=user.id).values_list('query_id', flat=True)
        q = Query.objects.filter(id__in=q)
        template = loader.get_template('website/urs.html')
        context = {

        'user':user,
        'i':q,
        }

        r = template.render(context, request)
        return HttpResponse(r)
    else:
        return HttpResponse('''You are not logged in .please <a href="/login">login</a>''')
def topics(request):
    q = Query.objects.filter(is_public=True).exclude(is_active=False)
    template = loader.get_template('website/topics.html')
    context = {
        'query': q,
    }

    r = template.render(context, request)
    return HttpResponse(r)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('website/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send(fail_silently=False)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'website/signup.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        template = loader.get_template('website/confirmed.html')
        context = {
        }
        r = template.render(context, request)
        return HttpResponse(r)
    else:
        return HttpResponse('Activation link is invalid!')

def results(request,query_id):
    q = SocialDataQuery.objects.filter(query__id=query_id).values_list('socialdata', flat=True)
    q=SocialData.objects.filter(id__in=q)
    s=""
    for data in q:
        s=s+data.message
    blob = TextBlob(s)
    s=blob.noun_phrases
    y=0
    wordlist = s
    for x in wordlist:
        y=y+1
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))
    wordlistn=[]
    wordfreqn=[]
  #  for i in range (0,y):
  #      for j in range (i+1,y):
  #          if(wordfreq[i]<wordfreq[j]):
  #              temp=wordlist[i]
  #              temp1=wordfreq[i]
   #             wordlist[i]=wordlist[j]
  #              wordfreq[i]=wordfreq[j]
   #             wordlist[j]=temp
  #              wordfreq[j]=temp1

  #  for i in range(0,10):
  #      wordlistn[i]=wordlist[i]
  #      wordfreqn[i]=wordfreq[i]
    aaa = zip(wordlist, wordfreq)

    #  for i in range(0,10):
  #      print (wordlist[i],wordfreq[i])
    #print("Pairs\n" + str(zip(wordlist, wordfreq)))

    topic=Query.objects.get(id=query_id)
    total_posts=q.count()
    q1 = SocialDataQuery.objects.filter(query__id=query_id).values_list('socialdata', flat=True)
    q1 = SocialData.objects.filter(id__in=q,source='FB')
    total_fb_data=q1.count()
    q2 = SocialDataQuery.objects.filter(query__id=query_id).values_list('socialdata', flat=True)
    q2 = SocialData.objects.filter(id__in=q).filter(source="TWITTER")
    total_twitter_data=q2.count()
    q3=q.filter(sentiment="HighNegative")
    hn_count=q3.count()
    n_count = q.filter(sentiment="Negative").count()
    nue_count = q.filter(sentiment="Nuetral").count()
    p_count = q.filter(sentiment="Positive").count()
    hp_count = q.filter(sentiment="HighPositive").count()
    if topic.is_public==True:
        template = loader.get_template('website/result.html')
        context = {
            'total_count': total_posts,
            'fb_count': total_fb_data,
            'twitter_count': total_twitter_data,
            'hn_count': hn_count,
            'n_count': n_count,
            'nue_count': nue_count,
            'p_count': p_count,
            'hp_count': hp_count,
            'fb_data': q1,
            'twitter_data': q2,
            'topic': topic,
            'result':aaa
        }
        r = template.render(context, request)
        return HttpResponse(r)
    else :
        user = request.user
        q = User.objects.filter(username=user)
        p = Token.objects.filter(user_id=user.id).values_list('query_id', flat=True)
        r = Query.objects.filter(id__in=p)
        s = Token.objects.filter(query_id=query_id)
        today = datetime.datetime.now().date()
        for data in s:
            validity=data.validity
            if(today>validity):
                data.is_active=False
                data.save()
        if q and topic in r and data.is_active==False:
            template = loader.get_template('website/js.html')
            context = {
                'valid': data,
                'topic': topic,
                'i': r,
                'qid':query_id,

            }

            r = template.render(context, request)
            return HttpResponse(r)
        if q and topic in r and data.is_active==True:
            template=loader.get_template('website/userresult.html')
            context = {
                'total_count': total_posts,
                'fb_count': total_fb_data,
                'twitter_count': total_twitter_data,
                'hn_count': hn_count,
                'n_count': n_count,
                'nue_count': nue_count,
                'p_count': p_count,
                'hp_count': hp_count,
                'fb_data': q1,
                'twitter_data': q2,
                'topic': topic,
                'i': r,
                'valid': data,
                'result': aaa
            }
            r = template.render(context, request)
            return HttpResponse(r)

        else:
            return HttpResponse('''Request error:private surveys visible for their owners <br> You are not logged in .please <a href="/login">login</a>for your survey''')


class customlogin(LoginView):
    template_name="website/login.html"
    def get_success_url(self):
       if self.request.user.is_superuser:
           return "/admin"
       else :
           return super(customlogin, self).get_success_url()


def payments(request):

    template = loader.get_template('website/js.html')
    context = {

    }

    r = template.render(context, request)
    return HttpResponse(r)


def checkout(request,query_id):
    s =Token.objects.filter(query_id=query_id)
    if request.method == "POST":
        tok  = request.POST.get("stripeToken")
    try:

        charge  = stripe.Charge.create(
            amount      = 33300,
            currency    = "INR",
            source      = request.POST.get("stripeToken"),
            description = "The product charged to the user"
            )
        for new_status in s:
            validity=new_status.validity+datetime.timedelta(days=30)
            new_status.is_active=True
            new_status.validity=validity
            new_status.transaction_id=charge.id
    except stripe.error.CardError as ce:
        return False, ce

    else:
        new_status.save()
        return HttpResponse('PAYMENT IS SUCCESSFUL AND YOUR SURVEY WILL BE CONTINUED<br>click <a href="/user">Here</a>to go back')


def add(request):
    if request.method == 'POST':
        form = Requestform(request.POST)
        if form.is_valid():
            input=["","","","","","","",""]
            option=["","","","","","",""]
            topicname = form.cleaned_data.get('Topicname')
            input[2] = form.cleaned_data.get('input2')
            option[2] = form.cleaned_data.get('option2')
            input[3] = form.cleaned_data.get('input3')
            option[3]= form.cleaned_data.get('option3')
            input[4] = form.cleaned_data.get('input4')
            option[4] = form.cleaned_data.get('option4')
            input[5] = form.cleaned_data.get('input5')
            option[5] = form.cleaned_data.get('option5')
            input[6] = form.cleaned_data.get('input6')
            query='"'+input[2]+'"'+option[2]+'"'+input[3]+\
                  '"'+option[3]+'"'+input[4]+'"'+option[4]+'"'+input[5]+'"'+option[5]+\
                  '"'+input[6]+'"'
            query=query.replace("NONE","")
            query=query.replace('""',"")
            request.session['query']=query
            request.session['name']=topicname
        return HttpResponse('The Query you have entered is'+query+'.<a href="/fixquery/">continue.</a>')

    else:
        form = Requestform()
        return render(request, 'website/user.html', {'form': form})
def fix(request):
    query= request.session['query']
    id=request.user
    name=request.session['name']
    t=Query(is_public=False,query=query,is_active=True,name=name)
    t.save()
    query_id=t
    token=account_activation_token.make_token(request.user)
    validity=datetime.datetime.now()+datetime.timedelta(days=30)
    q=Token(user=id,token=token,query=query_id,is_active=True,validity=validity)
    q.save()
    return HttpResponse('goto <a href="/user/">user home </a>')

'''SELECT *                                       
FROM   ts_stat($$SELECT to_tsvector('english', message) FROM website_socialdata$$) 
ORDER  BY ndoc DESC
LIMIT  10;'''