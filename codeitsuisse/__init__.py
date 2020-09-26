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
import codeitsuisse.routes.social_distance
import codeitsuisse.routes.olympiad_of_babylon
import codeitsuisse.routes.optimized_portfolio
import codeitsuisse.routes.bored_scribe
import codeitsuisse.routes.magical_fruit_basket
import codeitsuisse.routes.slms
import codeitsuisse.routes.bucket_fill
