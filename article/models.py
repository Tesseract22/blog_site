from email.policy import default
from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.


class Article(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    def cover_location(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s_%s.%s" % (instance.author.id, instance.created, ext)
        return "img/article_cover/%s"%filename

    cover = models.ImageField(upload_to=cover_location, default="img/article_default.jpg")

    class Meta():
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title

    