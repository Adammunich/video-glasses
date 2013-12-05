#C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"
#C:\windows\system32\cmd.exe /K "$(FULL_CURRENT_PATH)"

import numpy as np
import cv2
import os
import common

video_srcL = 3
video_srcR = 1

print " __      _       __              _____ _ "
print " \ \    / (_)   | |             / ____| |   "
print "  \ \  / / _  __| | ___  ___   | |  __| | __ _ ___ ___  ___  ___  "
print "   \ \/ / | |/ _` |/ _ \/ _ \  | | |_ | |/ _` / __/ __|/ _ \/ __| "
print "    \  /  | | (_| |  __/ (_) | | |__| | | (_| \__ \__ \  __/\__ \ "
print "     \/   |_|\__,_|\___|\___/   \_____|_|\__,_|___/___/\___||___/ "

print "\n ...for James"
print "\n Wash in the pool of Siloam"

print "\n\n\n\n\n Right video source: camera # "+str(video_srcR)
print " Left video source: camera # "+str(video_srcL)

window_width = 1260;
window_height = int((float(4/3) * float(window_width)));

cv2.namedWindow('videobox', 2)
cv2.resizeWindow('videobox', window_width, window_height)
cv2.moveWindow('videobox', 0, 0)

camL = cv2.VideoCapture(int(video_srcL))
camR = cv2.VideoCapture(int(video_srcR))


print camL.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600.0)
print camL.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800.0)

print camR.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600.0)
print camR.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800.0)

#print camL.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
#print camL.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
 
#camR = cv2.VideoCapture(video_srcR)

#right_frame = camR.read()

cv2.namedWindow('videobox')

#cv2.namedWindow('sliders')
#cv2.createTrackbar('thrs1', 'sliders', 2000, 5000, nothing)
#cv2.createTrackbar('thrs2', 'sliders', 4000, 5000, nothing)

showedge = 0
edge_thrsh_1 = 1500
edge_thrsh_2 = 2000

while True:
    ret, right_frame = camR.read()     # Nab a frame of video stream
    ret, left_frame = camL.read()
    #print camL.get(cv2.cv.CV_CAP_PROP_FPS)
    
    #right_frame = np.zeros_like(left_frame)   # There is no right camera yet :-(
    
    #thrs1 = cv2.getTrackbarPos('thrs1', 'sliders')
    #thrs2 = cv2.getTrackbarPos('thrs2', 'sliders')

    #right_frame = cv2.Canny(right_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)
    #left_frame = cv2.Canny(left_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)

    if(showedge):
        right_edge = cv2.Canny(right_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)
        left_edge = cv2.Canny(left_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)
    
        right_frame[right_edge != 0] = (0,255,255)
        left_frame[left_edge != 0] = (0,255,255)
    
    #right_frame = np.split(right_frame, 2, axis=1)[0]
    #left_frame = np.split(left_frame, 2, axis=1)[0]
    
    focal_length = 600; # This is the focal length of the lens, measured in pixels
    x_offset = 800/2;
    y_offset = 600/2;
    
    cameraMatrix = np.matrix([[focal_length, 0, x_offset], [0, focal_length, y_offset], [0, 0, 1]])
    
    vertical_smear_right = -0.1; # Variable names imply I haven't a clue what I'm doing yet
    vertical_smear_left = 0.1;
    
    horizontal_smear_right = 0;
    horizontal_smear_left = 0;
    
    fish_eye_ness_right = 0.2;
    fish_eye_ness_left = 0.2;
    
    smaller_fish_eye_ness_right = 8;
    smaller_fish_eye_ness_left = 8;
    
    distCoeffs_right = np.matrix([fish_eye_ness_right, smaller_fish_eye_ness_right, vertical_smear_right, horizontal_smear_right])
    distCoeffs_left = np.matrix([fish_eye_ness_left, smaller_fish_eye_ness_left, vertical_smear_left, horizontal_smear_left])
    
    right_frame = cv2.undistort(right_frame, cameraMatrix, distCoeffs_right)
    left_frame = cv2.undistort(left_frame, cameraMatrix, distCoeffs_left)
    
    right_frame = np.rot90(right_frame, 3) # Fix rotation issues
    left_frame = np.rot90(left_frame, 1)
    
    video_out = np.concatenate((left_frame, right_frame), axis=1)
    
    cv2.imshow('videobox', video_out)
    
    ch = 0xFF & cv2.waitKey(1)

    if ch == ord('e'):
        showedge = not showedge

cv2.destroyAllWindows() 
