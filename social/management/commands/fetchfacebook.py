from django.core.management.base import BaseCommand
from textblob import TextBlob
from website.models import SocialData,FbQueryMapper
import facebook, datetime

class Command(BaseCommand):

        def handle(self, *args, **options):
            q= FbQueryMapper.objects.all().exclude(id=2)
            for fbquerymapper in q :
                print fbquerymapper.page
                token = "741011062769592|tLH6FvFILJ0oOqoHGUKouycRuR4"
                since = datetime.datetime.now() - datetime.timedelta(days=14)
                d = since.date()
                graph = facebook.GraphAPI(token)
                data_set = graph.request(str(fbquerymapper.page)+
                '/posts?fields=description,message,created_time,shares,link,from,'                                      
                ' type,comments.summary(true),'
                'reactions.type(LIKE).limit(0).summary(total_count).as(reactions_like),'
                'reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love),'
                'reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow),'
                'reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha),'
                'reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad),'
                'reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry),'
                'reactions.type(THANKFUL).limit(0).summary(total_count).as(reactions_thankful),'                                       
                ' reactions.summary(true)&limit=50&since=' + str(d))

                data_set = data_set['data']
                while data_set:
                    for data in data_set:
                        try:
                            shares= data["shares"]["count"]
                        except:
                            shares= 0
                        try:
                            message = data["message"]
                        except:
                            pass
                        print "\n"
    	                print "\n"
    	                print "USER    : ",data["from"]["name"]
                        print "SHARES  : ",shares
    	                print "like   : ",data["reactions_like"]["summary"]["total_count"]
                        print "Love   : ", data["reactions_love"]["summary"]["total_count"]
                        print "wow   : ", data["reactions_wow"]["summary"]["total_count"]
                        print "haha   : ", data["reactions_haha"]["summary"]["total_count"]
                        print "sad   : ", data["reactions_sad"]["summary"]["total_count"]
                        print "angry   : ", data["reactions_angry"]["summary"]["total_count"]
                        print "thankful   : ", data["reactions_thankful"]["summary"]["total_count"]
    	                print "Message : ",message
    	                print "date    : ",data["created_time"]
    	                print "id    : ",data['id']

                        text = message
                        blob = TextBlob(text)
                        i=0
                        sentiment=0
                        for sentence in blob.sentences:
                            sentiment=sentiment+sentence.sentiment.polarity
                            i=i+1
                        sentiment=sentiment/i
                        if (sentiment >= -0.1 and sentiment <= 0.1):
                            senti= "Nuetral"
                        elif (sentiment > 0.5):
                            senti= "HighPositive"
                        elif (sentiment > 0.0 and sentiment <= 0.5):
                            senti= "Positive"
                        elif (sentiment > -0.5 and sentiment < 0.0):
                            senti= "Negative"
                        else:
                            senti= "HighNegative"
                        c=SocialData(message= message,
                                 created_date= data["created_time"],
                                 sentiment= senti,
                                 source = "FB",
                                 location= "UNKNOWN",
                                 like_count= data["reactions_like"]["summary"]["total_count"],
                                 love_count=data["reactions_love"]["summary"]["total_count"],
                                 haha_count=data["reactions_haha"]["summary"]["total_count"],
                                 sad_count=data["reactions_sad"]["summary"]["total_count"],
                                 wow_count=data["reactions_wow"]["summary"]["total_count"],
                                 angry_count=data["reactions_angry"]["summary"]["total_count"],
                                 link = "https://facebook.com/" + data['id'],
                                 fbquerymapper=fbquerymapper,
                                 shares= shares,
                                 thankful_count= data["reactions_thankful"]["summary"]["total_count"],
                                 )
    	                try:
                            c.save();
                            #("Continue...")
    	                except:
                            pass
                    data_set=False
                   # if (request.get(data["paging"]["next"])):
                   #     data_set = request.get(data["paging"]["next"])
                    #data_set = data_set['data']
