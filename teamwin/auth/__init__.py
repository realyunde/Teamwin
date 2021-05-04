from ..user.models import User

_USERID_KEY = '_tw_userid'


def login(request, userid):
    request.session[_USERID_KEY] = userid


def logout(request):
    request.session.clear()
    request.session.flush()


def is_authenticated(request):
    userid = request.session.get(_USERID_KEY)
    if userid is None:
        return False
    return User.user_exists(userid)


def get_current_user(request):
    userid = request.session.get(_USERID_KEY)
    return User.get_by_id(userid)
