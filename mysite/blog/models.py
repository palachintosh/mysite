from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.core.exceptions import ValidationError

def gen_slug(s):
    #new_slug = slugify(s, allow_unicode=True)
    print(s)
    s.lower() 
    format_string = slugify(s, allow_unicode=True)
    s_translate = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', '0': '0', '1': '1', '2': '2',
        '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
        }

    s_encode = []

    for i in format_string:
        try:
            if i == '-' or i == '_':
                s_encode.append(i)
            s_encode.append(s_translate.get(i, i))
                #s_encode.append(s_translate[i])
        except:
            raise ValidationError("Slug can't be generated!")
    new_slug = ''.join(map(str, s_encode))
    print(s_encode, new_slug)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):

    lang_choice = [
        ('PL', 'Polski'),
        ('RU', 'Russian'),
    ]

    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    description = models.TextField(blank=True, db_index=True, max_length=800, verbose_name="Preview")
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    post_picture = models.ImageField(upload_to="images/post_images/", db_index=True, default="")
    lang_filter = models.CharField(verbose_name="Site side: ", max_length=2, choices=lang_choice, blank=True, default='RU')
    like = models.SmallIntegerField(verbose_name="Likes", default=0, blank=True)

    related_post = models.ManyToManyField('self', blank=True, related_name='related_posts')

    # ManyToMany class instanse
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    
    #comments = models.ForeignKey(Comment, models.SET_NULL, blank=True, null=True)
    #comment_key = models.ForeignKey(Comment, on_delete=models.CASCADE)

    #tags = models.ManyToManyField(CommonTag)

    def get_absolute_url(self):
        return reverse('post_page_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})
    
    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})
    

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):

    name = models.CharField(max_length=20)
    comment_body = models.TextField(max_length=500)
    #time_date_pub = models.DateTimeField(auto_now_add=True)
    #user_email = models.EmailField()

    #foreignKey
    comments = models.ForeignKey(Post, models.SET_NULL, blank=True, null=True)
    #comment_key = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.tag_title)
    
    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})
    
    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})
    


def get_filter_url():
    return reverse('filter_form_url')


class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=200)
    privacy = models.TextField()