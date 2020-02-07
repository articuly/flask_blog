from libs import db
from models import User, Article
import random


def create_admin():
    user = User(realname='admin', username='admin', password='123654', sex='1', city='020', hobby='writing',
                intro='administrator')
    db.session.add(user)
    db.session.commit()


def create_random_user(n):
    words = list('abcdefghijklmnopqrstuvwxyz')
    cities = ['010', '020', '021', '023', '0755', '0571', '0512']
    hobbies = ['travel', 'reading', 'singing', 'dancing', 'writing', "swimming", "playing basketball"]
    for i in range(n):
        random.shuffle(words)
        username = ''.join(words[:6])
        sex = random.randint(0, 1)  # 0 for female, 1 for male
        city = cities[random.randint(0, 6)]
        random.shuffle(hobbies)
        hobby = ', '.join(hobbies[0:random.randint(0, 6)])
        user = User(
            realname='-',
            username=username,
            password='123654',  # default password is 123654
            sex=sex,
            city=city,
            hobby=hobby,
            intro=''
        )
        db.session.add(user)
    db.session.commit()

def create_random_article(n):
    words = list('abcdefghijklmnopqrstuvwxyz')
    for i in range(n):
        random.shuffle(words)
        title = ''.join(words[:6])
        intro= 'test for ' + title
        author = 'admin'
        content= ''.join(words)
        article = Article(
            title=title,
            intro=intro,
            author=author,
            content=content
        )
        db.session.add(article)
    db.session.commit()
