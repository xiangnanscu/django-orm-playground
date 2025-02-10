from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Min, Max, F, Q, Value, ExpressionWrapper, DecimalField, IntegerField
from django.db.models.functions import Coalesce, Extract, Now, Concat, Cast
from django.http import HttpResponse
from .models import *
from django.utils.safestring import mark_safe
import sqlparse
import re
import os

def highlight_sql(sql):
    sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
    return mark_safe(sql)

init_query = '''
Blog.objects.alias(entries=Count("entry")).annotate(entries=F("entries"))
'''
def index(request):
    query_str = request.GET.get('q', init_query)
    queryset = eval(query_str)
    sql = str(queryset.query)
    formatted_sql = highlight_sql(sql)
    current_dir = os.path.dirname(__file__)
    models_path = os.path.join(current_dir, 'models.py')
    with open(models_path, 'r') as f:
        models_content = f.read()

    return render(request, 'example/index.html', {
        'query_str': query_str,
        'sql': formatted_sql,
        'models_content': models_content
    })
