from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'main.html')

def daily_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
        select
          strftime('%Y-%m-%d', connected_at) dtick,
          count(1) cnt
        from logview_logrecord
          where datetime(connected_at) >= datetime('now', '-6 months')
        group by 1
        order by 1;
        """)
        data = [{'date': x[0], 'count': x[1]} for x in cursor.fetchall()]
    return JsonResponse(data, safe=False)

