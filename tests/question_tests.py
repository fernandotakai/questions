from models import User
from models import Question
from nose import with_setup

def setup():
    User.collection.remove({})
    Question.collection.remove({})

    assert User.all({}).count() == 0
    assert Question.all({}).count() == 0
 
@with_setup(setup)
def test_get_user():
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

    user_from_question = q.get_user()

    assert user_from_question._id == user._id

    q.user = u"anon!"

    q.save()

    assert not q.get_user()

@with_setup(setup)
def test_get_author():
    user = User()
    user.username = u"test"
    user.set_password("test123")

    assert user.save()
    assert user._id

    q = Question()
    q.question = u"test"
    q.author = user.username
    q.user = user.username

    assert q.save(validate=True)
    assert q._id
 
    author_from_question = q.get_author()

    assert author_from_question
    assert author_from_question._id == user._id
