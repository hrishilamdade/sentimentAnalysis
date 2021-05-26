from django.shortcuts import render
from django.http import HttpResponse
from .apps import SentimentanalyserConfig
from textblob import TextBlob
from .models import Mentions
from .models import Responses
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def home(request):
    def respond(polarity):
        if (polarity<-0.1):
            if(polarity>-0.5):
                return ["So sorry to hear that! We are constantly trying to improve our services. Do give us another chance"]
            else:
                return ["Dear sir/madam, we regret this. We will get in touch to help you feel better right away, please be patient with us",0,0]
        elif (polarity>=-0.15 and polarity<=0.2):
            if(polarity>=0):
                return ["Hello. We are here to help.",0,0]
            else:
                return ["Your feedback has been noted",0,0]
        else:
            if(polarity<0.5):
                return["",1,0]
            elif(polarity<0.75):
                return["We are so glad to hear you are enjoying! Have a great day!",1,0]
            else:
                return["As a company, we feel a lot better when our customers wake up in a positive way. Your services mean a lot to us. Much appreciated.",0,1]
    text=request.POST.get('data','')
    if(text==''):
        text='-'
        reply='-'
        sentiment='-'
        prediction='-'
    else:
        '''text=TextBlob(text)
        prediction=text.sentiment.polarity
        prediction=round(prediction,2)
        reply=respond(prediction)[0]
        if prediction<0:
            sentiment='Negative'
        elif prediction==0:
            sentiment='Neutral'
        else:
            sentiment='Positive '''
        sentiment_obj=SentimentIntensityAnalyzer()
        sentiment_dict=sentiment_obj.polarity_scores(text)
        prediction=sentiment_dict['compound']
        reply=respond(prediction)[0]
        if sentiment_dict['compound'] >= 0.05 :
            sentiment="Positive"
        elif sentiment_dict['compound'] <= - 0.05 :
            sentiment="Negative"
        else :
            sentiment="Neutral"
    return render(request,'index.html',{'text':text,'result':reply,'polarity':prediction,'sentiment':sentiment})


def bot(request):
    polarities=Mentions.objects.all().values('polarity')
    p,n,nl,t=0,0,0,0
    range=[]
    for i in polarities:
        range.append(t)
        t+=1
        if i['polarity'] >= 0.05:
            p+=1
        elif i['polarity'] <=-0.05:
            n+=1
        else:
            nl+=1
    subjectivities=Mentions.objects.all().values('subjectivity')
    subjectivities=[i['subjectivity'] for i in subjectivities]
    dict1=[p,n,nl]
    data={'polarity':dict1,'subjectivity':subjectivities,"range":range}
    return render(request,'bot.html',data)


def mention(request):
    query=request.POST.get('query','')
    value=request.POST.get('val','')
    if value=="":
        mention=Mentions.objects.all()
    else:
        if(query=="sender"):
            mention=Mentions.objects.filter(sender=value)
        elif(query=="polarity"):
            value=float(value)
            q='SELECT * FROM Mentions WHERE polarity BETWEEN %f AND %f'%(value-0.05,value+0.05)
            mention=Mentions.objects.raw(q)
        elif(query=="subjectivity"):
            value=float(value)
            mention=Mentions.objects.raw('SELECT * FROM Mentions WHERE subjectivity BETWEEN %f AND %f'%(value-0.05,value+0.05))
    l=len(mention)
    if(l>1):
        s=str(l)+" rows selected"
    else:
        s=str(l)+" row selected"
    return render(request,'mentions.html',{'mention':mention,'s':s})


def response(request):
    query=request.POST.get('query','')
    response=Responses.objects.all()
    if query=='is_liked':
        response=Responses.objects.filter(is_liked=1)
    elif query=='is_retweet':
        response=Responses.objects.filter(is_rt=1)
    return render(request,'responses.html',{'response':response})