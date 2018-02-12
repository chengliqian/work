from flask import Blueprint

auth = Blueprint('auth', __name__)
mointor = Blueprint('mointor', __name__)
case = Blueprint('case', __name__)
url = Blueprint('url', __name__)
dashboard = Blueprint('dashboard', __name__)

from . import auth_controller
from . import server_monitor_controller
from . import case_controller
from . import url_controller
from . import dashboard_controller
