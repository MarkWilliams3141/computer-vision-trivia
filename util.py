
def detect_question(image):
    special_pixel = image[16, 185]
    threshold = 20
    pixel_v_0 = 211
    pixel_v_1 = 232
    pixel_v_2 = 60

    p1 = False
    p2 = False
    p3 = False

    if (abs(pixel_v_0 - special_pixel[0]) < threshold):
        p1 = True

    if (abs(pixel_v_1 - special_pixel[1]) < threshold):
        p2 = True

    if (abs(pixel_v_2 - special_pixel[2]) < threshold):
        p3 = True

    if (p1 and p2 and p3):
        return True

    print('->' + str(image[16, 185]))
    return False

