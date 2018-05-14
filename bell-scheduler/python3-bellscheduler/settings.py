import sys
import os

relative_path = os.path.dirname(sys.modules[__name__].__file__)
RSRC_DIR = os.path.join(relative_path,'rsrc')
TEXT_DOMAIN = "bell-scheduler"
