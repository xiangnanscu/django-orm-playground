from django.shortcuts import render
from django.db.models import Count, Sum
from django.http import HttpResponse
from .models import Author, Article
from django.utils.safestring import mark_safe
import sqlparse
import re
import os

def highlight_sql(sql):
    # 格式化SQL
    sql = sqlparse.format(sql, reindent=True, keyword_case='upper')


    return mark_safe(sql)

def index(request):
    query_str = request.GET.get('q', "Author.objects.annotate(article_count=Count('articles')).filter(article_count__gt=2)")
    queryset = eval(query_str)
    sql = str(queryset.query)
    # 格式化并高亮SQL
    formatted_sql = highlight_sql(sql)

    # 读取models.py的内容
    current_dir = os.path.dirname(__file__)
    models_path = os.path.join(current_dir, 'models.py')
    with open(models_path, 'r') as f:
        models_content = f.read()

    return render(request, 'example/index.html', {
        'query_str': query_str,
        'sql': formatted_sql,
        'models_content': models_content
    })

# Create your views here.
