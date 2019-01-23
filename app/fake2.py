from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post

def users(count=100):
	fake = Faker()
	i=0
	while i<count:
		u = User(email=fake.email(),
			username=fake.user_name(),
			password=fake.password(),
			confirmed=True,
			name=fake.name(),
			location=fake.city(),
			about_me=fake.text(),
			member_since=fake.past_date())
		db.session.add(u)
		try:
			db.session.commit()
			i += 1
		except IntegrityError:
			db.session.rollback()

def posts(count=100):
	fake=Faker()
	user_count = User.query.count()
	for i in range(count):
		u = User.query.get(randint(1,user_count))
		p = Post(body=fake.text(),author=u,timestamp=fake.past_date())
		db.session.add(p)
	db.session.commit()

			
	
