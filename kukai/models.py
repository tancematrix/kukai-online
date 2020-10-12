from django.db import models

# Create your models here.

class Unza(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    unza_title = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    info = models.CharField(max_length=200, default="")
    toku_closed = models.BooleanField(default=False)
    senku_closed = models.BooleanField(default=False)
    selectors = models.ManyToManyField('auth.User', blank=True, related_name="joined_kukai")
    def __str__(self):
        return self.unza_title
    def close_toku(self):
        self.toku_closed = True
    def close_senku(self):
        self.senku_closed = True
    

class Ku(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    unza = models.ForeignKey(Unza, on_delete=models.CASCADE)
    haiku_text = models.CharField(max_length=50)
    selectors = models.ManyToManyField('auth.User', blank=True, related_name="selected_ku_set")
    def __str__(self):
        return self.haiku_text
    def get_author(self):
        return self.author

