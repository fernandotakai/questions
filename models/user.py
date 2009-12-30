from mongokit import MongoDocument

from hashlib import sha256
from hmac import HMAC
import random

def encode_password(password, salt):
    hashed_password = str(password)

    for x in xrange(100):
        hashed_password = HMAC(hashed_password, salt, sha256).digest() 

    return hashed_password

class User(MongoDocument):
    db_name = "questions"
    collection_name = "users"

    structure = dict(
        username=unicode,
        password=unicode
    )

    use_dot_notation=True
    required_fields =  ['username', 'password']

    def unanswered_questions(self):
        return Question.all({ 'user': self.username, 'answer': None })

    def answered_questions(self):
        return Question.all({ 'user': self.username, 'answer': {'$exists': True} })

    def set_password(self, password):
        salt = "".join(chr(random.randrange(256)) for i in xrange(8))

        hashed_password = encode_password(password, salt)
        
        self.password = unicode(salt.encode("base64").strip()) + u"," + unicode(hashed_password.encode("base64").strip())

    def verify_password(self, password):
        salt, hashed_password = self.password.split(",")

        salt = salt.decode("base64")
        hashed_password = hashed_password.decode("base64")

        return hashed_password == encode_password(password, salt)

from question import Question
