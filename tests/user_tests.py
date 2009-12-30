from models import User
from models import Question
from nose import with_setup

def setup():
    User.collection.remove({})
    Question.collection.remove({})

    assert User.all({}).count() == 0
    assert Question.all({}).count() == 0
 
@with_setup(setup)
def test_verify_password():
    user = User()
    user.username = u"test"
    user.set_password('test1234')

    user.save()

    assert user.verify_password('test1234')
    assert not user.verify_password('test')

@with_setup(setup)    
def test_get_unanswered_questions():
    user = User()
    user.username = u"test"
    user.set_password("test123")

    assert user.save()
    assert user._id

    q = Question()
    q.question = u"test"
    q.author = u"anon"
    q.user = user.username

    assert q.save(validate=True)
    assert q._id
     
    user_from_db = User.one({'username': 'test'})

    assert user_from_db.unanswered_questions().count() == 1

@with_setup(setup)    
def test_get_answered_questions():
    user = User()
    user.username = u"test"
    user.set_password("test123")

    assert user.save()
    assert user._id

    q = Question()
    q.question = u"test"
    q.author = u"anon"
    q.answer = u"My Answer!"
    q.user = user.username

    assert q.save(validate=True)
    assert q._id
     
    user_from_db = User.one({'username': 'test'})

    assert user_from_db.answered_questions().count() == 1
