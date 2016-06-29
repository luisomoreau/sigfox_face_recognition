#import packages
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
from sigfox import sendsigfox

#init the picamera
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#init display
lcdDisplay = True
if lcdDisplay:
        d = display.Display(SMBus(1))
        d.move(0, 0)
        light = backlight.Backlight(SMBus(1), 0x62)
        light.set_color(0, 0, 0)
        print 'Display ready'
else:
        print 'No display'

#init opencv
faceCascade = cv2.CascadeClassifier("opencv/haarcascade_frontalface_default.xml")
if lcdDisplay:
        d.write("Loading data")
else:
        print 'Loading training data...'
if lcdDisplay:
        d.write("Setting up")
else:
        print "Setting up"
model = cv2.createEigenFaceRecognizer()
model.load("opencv/training.xml")
if lcdDisplay:
        d.write("Ready")
else:
        print "Training data ready"

#Init Sigfox
sgfx = sendsigfox.Sigfox("/dev/ttyAMA0")
ids = []
t0 = time.time()
intervall = 10 *60 #10 min * 60 sec

# loop over the frames from the video stream
while True:
	time.sleep(2)
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
                if label == config.LOUIS_LABEL and confidence < 2500:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)                        
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hello Louis".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
                elif label == config.ANTHO_LABEL and confidence < 2500:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)                        
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hello Antho".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
                elif label == config.NICO_LABEL and confidence < 2500:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hello Nico".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
                elif label == config.BATISTE_LABEL and confidence < 2200:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hello Batiste".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
		elif label == config.LOURDES_LABEL and confidence < 2800:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)                        
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hola Lourdes".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
		elif label == config.NADINE_LABEL and confidence < 2500:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hi Nadine".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)
		elif label == config.ANAMARIA_LABEL and confidence < 2800:
                        #print 'Recognized face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        if lcdDisplay:
                                light.set_color(0, 255, 0)
                                d.move(0, 0)
                                d.write("Hi Ana Maria".format(label))
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                ids.append(label)

                else:
                        #print 'Did not recognize face!'
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        if lcdDisplay:
                                light.set_color(0, 0, 0)
                                d.move(0, 0)
                                d.write("Hi handsome")
                        else:
                                print "Hello {0} - confidence {1}".format(label, confidence)
                        if ids.count(label) == 0 and len(ids) < 12:
                                if confidence < 2000:
                                        ids.append(label)
                                else:
                                        ids.append(1)
                

        # show the frame
        if lcdDisplay:
                d.write("                   ")
                d.write("                   ")
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if len(ids) != 0:
                message = ''.join(format(id, '02d') for id in ids)
                #print message
                t1 = time.time()
       
                if (t1-t0) >= intervall:
                        if lcdDisplay:
                                light.set_color(0, 0, 255)
                                d.write("Sending Sigfox")
                                d.write(message)
                        sgfx.sendMessage(message)
                        t0 = time.time()
                        ids = []
                        if lcdDisplay:
                                light.set_color(0, 0, 0)
                                d.write("                   ")
                                d.write("                   ")

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                if lcdDisplay:
                        light.set_color(0, 0, 0)
                break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
