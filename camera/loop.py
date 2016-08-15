from six.moves import cStringIO as StringIO
from PIL import Image
import datetime
import sys

state = {}

def start():
    if len(sys.argv) != 2:
        raise ValueError("Usage: -s 'loop.py SECONDS'")
    state["secs"] = int(sys.argv[1])
    state["images"] = []
    state["index"] = 0
    print("Will loop %d second(s) of video" % state["secs"])
    
def response(flow):
    # start timer after first flow is seen
    state.setdefault("start",datetime.datetime.now())
    # look at images coming from snapshot.cgi
    if "snapshot.cgi" in flow.request.path and flow.response.headers.get("content-type", "").startswith("image"):
        if (datetime.datetime.now()-state["start"]).seconds > state["secs"]:
            try:
                # iterate through stored images and replace current
                flow.response.content = state["images"][state["index"]].getvalue()
                flow.response.headers["content-type"] = "image/jpeg"
                if state["index"] + 1 >= len(state["images"]):
                    state["index"] = 0
                else:
                    state["index"] += 1
            except:  # Unknown image types etc.
                pass
        else:
            try:
                # store image for later recall
                state["images"].append(StringIO(flow.response.content))
            except:
                pass
