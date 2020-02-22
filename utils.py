from libs import db
from models import User, Article
import random


# 创建admin用户，不受用户名要6位以上的限制
def create_admin():
    user = User(realname='admin', username='admin', sex='1', city='020', hobby='writing',
                intro='administrator')
    user.hash_password('123654')
    db.session.add(user)
    db.session.commit()


# 创建N个随机用户
def create_random_user(n):
    words = list('abcdefghijklmnopqrstuvwxyz')
    cities = ['010', '020', '021', '023', '0755', '0571', '0512']
    hobbies = ['travel', 'reading', 'singing', 'dancing', 'writing', "swimming", "playing basketball"]
    for i in range(n):
        random.shuffle(words)
        username = ''.join(words[:6])
        sex = random.randint(1, 2)  # 2 for female, 1 for male
        city = cities[random.randint(0, 6)]
        random.shuffle(hobbies)
        hobby = ', '.join(hobbies[0:random.randint(0, 6)])
        user = User(
            realname='-',
            username=username,
            sex=sex,
            city=city,
            hobby=hobby,
            intro=''
        )
        user.hash_password('123456')  # default password is 123456
        db.session.add(user)
    db.session.commit()


# 为某个作者创建N篇随机文章
def create_random_article(n, a):
    words = list('abcdefghijklmnopqrstuvwxyz')
    for i in range(n):
        random.shuffle(words)
        title = ''.join(words[:6])
        intro = 'test for ' + title
        author = a
        content = ''.join(words)
        cate_id = random.randint(1, 7)
        article = Article(
            title=title,
            intro=intro,
            author=author,
            content=content,
            cate_id=cate_id
        )
        db.session.add(article)
    db.session.commit()
