from six.moves import cStringIO as StringIO
from PIL import Image
from random import randint
import sys

state = {}

def start():
    if len(sys.argv) != 2:
        raise ValueError("Usage: -s 'static.py image_dir/'")
    state["dir"] = sys.argv[1]

def response(flow):
    # look at images coming from snapshot.cgi
    if "snapshot.cgi" in flow.request.path and flow.response.headers.get("content-type", "").startswith("image"):
        try:
            # replace current image with random "static" image
            # there are better ways to do this, but whatev
            path = "%s%08d.jpg" % (state["dir"],randint(1,249))
            img = StringIO(open(path, 'rb').read())
            flow.response.content = img.getvalue()
            flow.response.headers["content-type"] = "image/png"
        except:  # Unknown image types etc.
            pass

# © 2016, Trend Micro Incorporated
