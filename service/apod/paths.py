
import os

DIR_THIS = os.path.dirname(__file__)

class APodPaths:
    DIR_STATIC = os.path.join(DIR_THIS, "website", "static")
    DIR_RESULTS = os.path.expanduser(os.path.join("~", "akit", "results"))
    DIR_TEMPLATES = os.path.join(DIR_THIS, "website", "templates")
