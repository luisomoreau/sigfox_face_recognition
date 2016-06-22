# USAGE
# python videostream_demo.py
# python videostream_demo.py --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from smbus import SMBus
import datetime
import argparse
import imutils
import time
import cv2
from opencv import config
from opencv import face
from lcd import backlight
from lcd import screen
from lcd import display

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=1,
        help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

d = display.Display(SMBus(1))
d.move(0, 0)
light = backlight.Backlight(SMBus(1), 0x62)
light.set_color(0, 0, 0)
faceCascade = cv2.CascadeClassifier("opencv/haarcascade_frontalface_default.xml")
print 'Loading training data...'

d.write("Setting up")
model = cv2.createEigenFaceRecognizer()
model.load("opencv/training.xml")

print 'Training data loaded!'
d.write("Ready")

# loop over the frames from the video stream
while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
                # Crop and resize image to face.
                crop = face.resize(face.crop(gray, x, y, w, h))
                # Test face against model.
                label, confidence = model.predict(crop)
                
                #print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
                #        'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE',
                #        confidence)
                print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(label, confidence)
                if label == config.LOUIS_LABEL and confidence < 3000:
                        #print 'Recognized face!'
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        light.set_color(0, 255, 0)
                        d.move(0, 0)
                        d.write("Hello Louis".format(label))
                elif label == config.ANTHO_LABEL and confidence < 2600:
                        #print 'Recognized face!'
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        light.set_color(0, 255, 0)
                        d.move(0, 0)
                        d.write("Hello Antho".format(label))
                elif label == config.NICO_LABEL and confidence < 2600:
                        #print 'Recognized face!'
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        light.set_color(0, 255, 0)
                        d.move(0, 0)
                        d.write("Hello Nico".format(label))
                elif label == config.BATISTE_LABEL and confidence < 2200:
                        #print 'Recognized face!'
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        light.set_color(0, 255, 0)
                        d.move(0, 0)
                        d.write("Hello Batiste".format(label))
                else:
                        #print 'Did not recognize face!'
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        light.set_color(0, 0, 0)
                        d.move(0, 0)
                        #d.write("Do I know you?")
                

        # show the frame
        d.write("                   ")
        d.write("                   ")
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                light.set_color(0, 0, 0)
                break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
