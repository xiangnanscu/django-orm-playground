from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Min, Max, F, Q, Value, ExpressionWrapper, Case, When
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
current_dir = os.path.dirname(__file__)
models_path = os.path.join(current_dir, 'models.py')
with open(models_path, 'r') as f:
    models_content = f.read()

def index(request):
    query_str = request.GET.get('q', init_query)
    exec_mode = request.GET.get('exec_mode') == 'true'
    error_message = None
    formatted_sql = None

    try:
        if exec_mode:
            # In exec mode, execute code and expect the code to set the sql variable
            local_vars = {}
            exec(query_str, globals(), local_vars)
            if 'sql' not in local_vars:
                raise Exception("In exec mode, code must set the 'sql' variable")
            sql = str(local_vars['sql'])
        else:
            # In eval mode, evaluate expression and expect to get a queryset
            queryset = eval(query_str, globals())
            sql = str(queryset.query)
        formatted_sql = highlight_sql(sql)
    except Exception as e:
        error_message = str(e)

    return render(request, 'example/index.html', {
        'query_str': query_str,
        'sql': formatted_sql,
        'models_content': models_content,
        'error_message': error_message,
        'exec_mode': exec_mode
    })
