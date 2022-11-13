from email.policy import default
from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.


class Article(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # ���±��⡣models.CharField Ϊ�ַ����ֶΣ����ڱ���϶̵��ַ������������
    title = models.CharField(max_length=100)

    # �������ġ���������ı�ʹ�� TextField
    body = models.TextField()

    # ���´���ʱ�䡣���� default=timezone.now ָ�����ڴ�������ʱ��Ĭ��д�뵱ǰ��ʱ��
    created = models.DateTimeField(default=timezone.now)

    # ���¸���ʱ�䡣���� auto_now=True ָ��ÿ�����ݸ���ʱ�Զ�д�뵱ǰʱ��
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

    