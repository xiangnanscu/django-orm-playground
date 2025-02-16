from datetime import date

from django.db import models

# https://docs.djangoproject.com/en/dev/topics/db/queries/
# https://docs.djangoproject.com/en/dev/topics/db/aggregation/

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    data = models.JSONField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries', related_query_name='entry')
    reposted_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name='reposted_entries', related_query_name='reposted_entry')
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline

class ViewLog(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_query_name='view_log')
    ctime = models.DateTimeField(auto_now_add=True)


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)