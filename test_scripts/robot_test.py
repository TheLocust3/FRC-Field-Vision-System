import cv2
import cv
import numpy as np
import time

def bgr_normalize(im):
    for x in range(im.shape[1]):
        for y in range(im.shape[0]):
            red_value = float(im[y][x][2])
            green_value = float(im[y][x][1])
            blue_value = float(im[y][x][0])
            sum_color = red_value + green_value + blue_value
            if sum_color == 0:
                im[y][x] = [0, 0, 0]
            else:
                im[y][x][2] = red_value / sum_color * 255
                im[y][x][1] = green_value / sum_color * 255
                im[y][x][0] = blue_value / sum_color * 255

    return im

def get_contour_length(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return w

def get_contours_location(group):
    avg_y = 0
    avg_x = 0
    for contour in group:
        x, y, w, h = cv2.boundingRect(contour)
        avg_y += y
        avg_x += x

    avg_y /= len(group)
    avg_x /= len(group)

    return (avg_y, avg_x)

def get_avg_color(contour, im):
    pixels = []

    mask = np.zeros(im.shape, np.uint8)
    cv2.drawContours(mask, [contour], 0, (255, 255, 255), cv.CV_FILLED)
    pixelpoints = np.transpose(np.nonzero(mask))

    for i in xrange(0, len(pixelpoints), 10): # Skip over some pixels to hopefully make this more efficient
        color = im[pixelpoints[i][0]][pixelpoints[i][1]]
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

def is_blueish(color):
    if color[0] - 5 > color[1]:
        return False
    elif color[0] - 5 > color[2]:
        return False

    return True

def is_redish(color):
    if color[2] - 5 > color[1]:
        return False
    elif color[2] - 5 > color[0]:
        return False
        
    return True

# Group contours by contours that are horizontalish and verticalish with eachother
def group_contours(contours):
    MAX_Y_DIFFERENCE = 80
    MAX_X_DIFFERENCE = 50 # TODO: Make this based on a formula
    grouped_contours = [] # Format: each group is an array that consists of 0 -> mid_y, 1 -> mid_x, 2 -> array of each contour
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        mid_y = y + (h / 2)
        mid_x = x + (w / 2)

        i = 0
        found = False
        for group in grouped_contours:
            if mid_y < (group[0] + MAX_Y_DIFFERENCE) and mid_y > (group[0] - MAX_Y_DIFFERENCE):
                if mid_x < (group[1] + MAX_X_DIFFERENCE) and mid_x > (group[1] - MAX_X_DIFFERENCE):
                    found = True
                    break
            i += 1
        
        if found:
            grouped_contours[i][2].append(contour)
        else:
            grouped_contours.append([mid_y, mid_x, [contour]])

    return grouped_contours

# Get only contours with the right color and split up long contours
def find_robots(grouped_contours):
    robots = [] # 0 -> y, 1 -> x, 3 -> color
    for group in grouped_contours:
        y, x = get_contours_location(group[2])
        color = get_avg_color(np.vstack(group[2]), im)

        if is_redish(color) or is_blueish(color):
            length = get_contour_length(np.vstack(group[2]))
            if length > (0.6 * y):
                robots.append([y - (length / 2), x, color])
                robots.append([y + (length / 2), x, color])
            else:
                robots.append([y, x, color])

    return robots

def prepare_image(im):
    start_time = time.time()
    normalized_im = bgr_normalize(im)
    print("Normalize took " + str(time.time() - start_time))

    grey = cv2.cvtColor(normalized_im, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((1, 20), np.uint8)
    final_im = cv2.erode(thresh, kernel)
    final_im = cv2.dilate(final_im, kernel)

    return final_im

cap = cv2.VideoCapture('test_videos/match_video.mp4')

while(cap.isOpened()):
    ret, im = cap.read()
    im = im[0:300, 300:(im.shape[1] - 200)]
    #im = cv2.resize(im, (im.shape[1] / 2, im.shape[0] / 2))

    start_time = time.time()

#print("Reading image")
#im = cv2.imread('test2.png')

    print("Preparing image")
    final_im = prepare_image(im)

    print("Finding contours")
    contours, hierarchy = cv2.findContours(final_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("Grouping contours")
    grouped_contours = group_contours(contours)

    print("Finding robots")
    robots = find_robots(grouped_contours)

    # Draw it
    print("Drawing")
    for location in robots:
        cv2.rectangle(im, (location[1], location[0]), (location[1] + 5, location[0] + 5), (0, 0, 0), -1)

    print("Took " + str(time.time() - start_time))

    cv2.imshow('frame', im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cv2.imshow('grouped contours', im)
#cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
