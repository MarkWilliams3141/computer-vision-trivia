import time

import cv2
import mss
import numpy
import pytesseract
import datetime
from PIL import Image
import pprint
import re

def get_text_from_image(image):
    return pytesseract.image_to_string(image)


def detect_question_2(image):

    x_offset = 25
    white_count = 0
    threshold = 750

    for x in range(0, 300):

        pixel_sum_0 = int(image[310, x + x_offset][0]) + int(image[310, x + x_offset][1]) + int(image[310, x + x_offset][2])
        pixel_sum_1 = int(image[380, x + x_offset][0]) + int(image[380, x + x_offset][1]) + int(image[380, x + x_offset][2])
        pixel_sum_2 = int(image[450, x + x_offset][0]) + int(image[450, x + x_offset][1]) + int(image[450, x + x_offset][2])

        if pixel_sum_0 >= threshold:
            white_count += 1

        if pixel_sum_1 >= threshold:
            white_count += 1

        if pixel_sum_2 >= threshold:
            white_count += 1

        image[310, x + x_offset] = (0,255,0,255)
        image[380, x + x_offset] = (0, 255, 0, 255)
        image[450, x + x_offset] = (0, 255, 0, 255)

    if white_count > 650:
        return True

    return False


def get_strings(image):
    a = datetime.datetime.now()
    text = pytesseract.image_to_string(Image.fromarray(image))
    print(text)
    ocr_text_list = re.split(r'[\n]+', text)

    try:
        answer3 = ocr_text_list.pop()
        answer2 = ocr_text_list.pop()
        answer1 = ocr_text_list.pop()
        question = " ".join(ocr_text_list)
        b = datetime.datetime.now()
        delta = b - a
        print("{} ms elapsed".format(int(delta.total_seconds() * 1000)))

        return {
            'answer1': answer1,
            'answer2': answer2,
            'answer3': answer3,
            'question': question
        }

    except Exception as e:
        print(e)

with mss.mss() as sct:
    # Part of the screen to capture
    #monitor = {'top': 120, 'left': 1040, 'width': 370, 'height': 470}
    monitor = {'top': 100, 'left': 1040, 'width': 370, 'height': 480}
    currenttime =  datetime.datetime.now()
    next_ocr = currenttime + datetime.timedelta(seconds=3)

    while 'Screen capturing':
        last_time = time.time()
        currenttime =  datetime.datetime.now()

        if(currenttime > next_ocr):
            next_ocr = currenttime + datetime.timedelta(seconds=3)
            #print('3 seconds passed')


        #print('fps: {0}'.format(1 / (time.time() - last_time)))

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        cv2.rectangle(img, (0,0), (150,100),(0,255,0),-1)

        font1 = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText1 = (10, 40)
        fontScale1 = 0.5
        fontColor1 = (0, 0, 0)
        lineType1 = 2

        detected = detect_question_2(img)

        cv2.putText(img, 'Detected: ' + str(detected),
                    bottomLeftCornerOfText1,
                    font1,
                    fontScale1,
                    fontColor1,
                    lineType1)

        if detected:
            print(get_strings(img))
            exit()

        '''
        cv2.putText(img, 'Detected: ' + str(detect_question(img)),
                    bottomLeftCornerOfText1,
                    font1,
                    fontScale1,
                    fontColor1,
                    lineType1)
        '''


        # Write some Text

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 20)
        fontScale = 0.5
        fontColor = (0, 0, 0)
        lineType = 2

        cv2.putText(img, 'fps: {0:0.1f}'.format(1 / (time.time() - last_time)),
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)



        # Display the picture   myimg = Image.fromarray(img)
        #txt = pytesseract.image_to_string(myimg)
        #print(txt)

        cv2.imshow('OpenCV/Numpy normal', img)

        # Display the picture in grayscale
        #cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))



        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break