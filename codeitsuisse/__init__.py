from flask import Flask

app = Flask(__name__)

import codeitsuisse.routes.intelligent_farming
import codeitsuisse.routes.inventory_management
import codeitsuisse.routes.clean_floor
import codeitsuisse.routes.revisit_geometry
import codeitsuisse.routes.salad_spree
import codeitsuisse.routes.sort
import codeitsuisse.routes.square
import codeitsuisse.routes.contact_trace
import codeitsuisse.routes.cluster
