import os
from __future__ import absolute_import
from __future__ import annotations
from flask import Flask

# Instantiating Flask Object
app = Flask(__name__)

# Secret Key
app.config["SECRET_KEY"] = os.environ.get('PORTALIGN_SECRET_KEY')

from prolign import routes
