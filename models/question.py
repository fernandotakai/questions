from mongokit import MongoDocument
from user import User

from datetime import datetime

class Question(MongoDocument):
    db_name = "questions"
    collection_name = "questions"

    structure = dict(
        question=unicode,
        answer=unicode,
        author=unicode,
        user=unicode,
        created=datetime,
        answered=datetime
    )
    
    use_dot_notation=True
    required_fields = ['question', 'author', 'user']
    default_values = dict(created=datetime.utcnow)

    def get_user(self):
        return User.one({'username': self.user})

    def get_author(self):
        return User.one({'username': self.author})
