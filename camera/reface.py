from six.moves import cStringIO as StringIO
from PIL import Image
import sys
import numpy as np
import cv2

state = {}

def start():
    if len(sys.argv) != 3:
        raise ValueError("Usage: -s 'reface.py image_dir/ /path/to/haarcascade.xml'")
    state["new_faces"] = []
    # laziness...read all frames of laughing man animation into array
    for x in range(0,48):
        img = cv2.imread("%s%s.png" % (sys.argv[1],x),-1)
        state["new_faces"].append(img)
    state["facecasc"] = cv2.CascadeClassifier(sys.argv[2])
    state["faces"] = []
    state["idx"] = 0
    
def response(flow):
    # look at images coming from snapshot.cgi
    if "snapshot.cgi" in flow.request.path and flow.response.headers.get("content-type", "").startswith("image"):
        try:
            # process image into numpy array for opencv
            img_str = StringIO(flow.response.content).getvalue()
            nparr = np.fromstring(img_str, np.uint8)
            img = cv2.imdecode(nparr,cv2.CV_LOAD_IMAGE_COLOR)
            # convert to grayscale for better detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # find faces in image
            faces = state["facecasc"].detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            if len(faces) > 0:
                # update stored faces if new ones are found
                state["faces"] = faces
            for (x, y, w, h) in state["faces"]:
                # resize laughing man image to dimensions of face
                new_face = cv2.resize(state["new_faces"][state["idx"]],(w,h))
                # overwrite area of image with laughing man (compensating for alpha channel transparency)
                for c in range(0,3):
                    img[y:y + h,x:x + w,c] = new_face[:,:,c] * (new_face[:,:,3]/255.0) + img[y:y + h,x:x + w,c] * (1.0 - new_face[:,:,3]/255.0)
            # increment index for next frame of animation
            if state["idx"] < len(state["new_faces"]) - 1:
                state["idx"] += 1
            else:
                state["idx"] = 0
            # replace image with modified version
            flow.response.content = cv2.imencode('.jpg',img)[1].tostring()
            flow.response.headers["content-type"] = "image/jpeg"
        except:  # Unknown image types etc.
            pass

# © 2016, Trend Micro Incorporated
