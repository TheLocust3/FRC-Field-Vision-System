import cv2
import cv
import numpy as np

def bgr_normalize(image):
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            red_value = float(image[y][x][2])
            green_value = float(image[y][x][1])
            blue_value = float(image[y][x][0])
            sum_color = red_value + green_value + blue_value
            if sum_color == 0:
                image[y][x] = [0, 0, 0]
            else:
                image[y][x][2] = red_value / sum_color * 255
                image[y][x][1] = green_value / sum_color * 255
                image[y][x][0] = blue_value / sum_color * 255

    return image

def ostu_threshold(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh

def get_approx_contour_width(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return w

def get_approx_contours_location(group):
    avg_y = 0
    avg_x = 0
    for contour in group:
        x, y, w, h = cv2.boundingRect(contour)
        avg_y += y
        avg_x += x

    avg_y /= len(group)
    avg_x /= len(group)

    return (avg_y, avg_x)

def get_avg_contour_color(contour, image):
    pixels = []

    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [contour], 0, (255, 255, 255), cv.CV_FILLED)
    pixelpoints = np.transpose(np.nonzero(mask))

    for i in xrange(0, len(pixelpoints), 10): # Skip over some pixels to hopefully make this more efficient
        color = image[pixelpoints[i][0]][pixelpoints[i][1]]
        pixels.append([color[2], color[1], color[0]]) # BGR

    blue = 0
    green = 0
    red = 0

    for color in pixels:
        blue += color[0]
        green += color[1]
        red += color[2]

    blue /= len(pixels)
    green /= len(pixels)
    red /= len(pixels)

    return (blue, green, red)

def is_blueish(color, tolerance):
    if color[0] - tolerance > color[1]:
        return False
    elif color[0] - tolerance > color[2]:
        return False

    return True

def is_redish(color, tolerance):
    if color[2] - tolerance > color[1]:
        return False
    elif color[2] - tolerance > color[0]:
        return False
        
    return True
