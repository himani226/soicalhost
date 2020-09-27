from copy import deepcopy

from socialgram.models import UserProfileInfo

INVALID_SESSION_RESPONSE = {'status':False, 'results':{}, 'message':"Invalid Session, Please Login Again"}

_NO_SUCCESS_RESPONSE = {'status':False, 'results': {}}

_SUCCESS_RESPONSE = {'status':True}

def success_response():
    return deepcopy(_SUCCESS_RESPONSE)

def no_success_response():
    return deepcopy(_NO_SUCCESS_RESPONSE)

def authenticateUser(token):
    user = None
    try:
        user = UserProfileInfo.objects.filter(token=token).first()
        if not user:
            response = no_success_response()
            response['message'] = "Valid Token Not provided"
            return False, response
        if not user.ifLogged:
            return False, INVALID_SESSION_RESPONSE
    except Exception as e:
        response = no_success_response()
        response['message'] = "Some exception occured"
        return False, response
    return True, user