def main():
  from django.db.models import Count, Sum, Avg, Min, Max, F, Q, Value, ExpressionWrapper, Case, When
  Entry.objects.annotate(
      rating_level=Case(
          When(rating__gt=8, then=Value('高')),
          When(rating__gt=6, then=Value('中')),
          default=Value('低'),
          output_field=CharField()
      )
  )
main()

(lambda :Entry.objects.annotate(rating_level=Case(When(rating__gt=8, then=Value('高')),When(rating__gt=6, then=Value('中')),default=Value('低'),output_field=CharField())))()