from django.core.management.base import BaseCommand
from django.db import connection

from website.models import SocialDataQuery,Query

class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Query.objects.filter(is_active=True)
        for query in q:
            t=SocialDataQuery.objects.filter(query=query).values_list("socialdata__id",flat=True)
            s= query.query
            s = s.replace('"', "''")
            s = s.replace('AND', '&')
            s = s.replace('OR', '|')
            s = s.replace('-', '&!')
            s="'"+s+"'"
            print s
            with connection.cursor() as cursor:
                sql="SELECT id FROM website_socialdata WHERE message @@ to_tsquery("+s+")"
                cursor.execute(sql)
                row=cursor.fetchall()
                row=[x[0]for x in row]
                row=set(row)-set(t)
                if(row):
                    x="INSERT INTO website_socialdataquery(socialdata_id,query_id) VALUES"+",".join(["(%d,%d)"%(x,query.id)for x in row])
                    cursor.execute(x)


