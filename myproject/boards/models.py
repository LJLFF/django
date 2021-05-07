from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)#强制数据库级别字段的唯一性
    description = models.CharField(max_length=100)

    #返回中文名称
    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)#创建post对象时为当前日期和时间
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)#related_name关联模型
    #board是Board的外键 一个topic实例只涉及一个Board实例,related_name创建反向关系,Board实例通过属性topics访问该板块topic列表
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)#关联User模型表示是由谁创建的,related_name表示User可以用User.posts查看该用户创建了哪些帖子
    updated_by = models.ForeignKey(User, null=True, related_name='+',  on_delete=models.CASCADE)#+指示django不需要反向关系