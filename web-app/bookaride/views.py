
from .loginviews import *
from .profileviews import *
from .commonuserviews import *
from .driverviews import *


# main entry to login
def index(request):
    return render(request, 'oauth/index.html')



