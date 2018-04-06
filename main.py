import time

import cv2
import mss
import numpy
import pytesseract
import datetime
from PIL import Image
import re


def detect_state(image):

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


def draw_stuff(image, detected, last_ocr):

    reset = datetime.timedelta(seconds=10) - (datetime.datetime.now() - last_ocr)
    cv2.rectangle(image, (0, 0), (150, 100), (0, 255, 0), -1)
    font1 = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText1 = (10, 40)
    fontScale1 = 0.5
    fontColor1 = (0, 0, 0)
    lineType1 = 2

    cv2.putText(image, 'Detected: ' + str(detected),
                bottomLeftCornerOfText1,
                font1,
                fontScale1,
                fontColor1,
                lineType1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 20)
    fontScale = 0.5
    fontColor = (0, 0, 0)
    lineType = 2

    cv2.putText(image, 'fps: {0:0.1f}'.format(1 / (time.time() - last_time)),
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(image, 'reset: {0}'.format(reset.seconds),
                (10, 60),
                font,
                fontScale,
                fontColor,
                lineType)

def get_strings(image):
    a = datetime.datetime.now()

    # do ocr extraction with tesseract
    text = pytesseract.image_to_string(Image.fromarray(image))

    # remove any non-standard characters
    text = re.sub('[^A-Za-z0-9 \n]+', '', text)

    #print for good measure
    print(text)

    #split by new line char
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

    last_ocr = datetime.datetime.now() - datetime.timedelta(seconds=60)

    while 'Screen capturing':
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))
        detected = detect_state(img)

        draw_stuff(img, detected, last_ocr)

        if last_ocr + datetime.timedelta(seconds=10) <= datetime.datetime.now():
            if detected:
                last_ocr = datetime.datetime.now()
                print(get_strings(img))

        cv2.imshow('OpenCV/Numpy normal', img)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break