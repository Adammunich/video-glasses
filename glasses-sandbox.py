#C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"
#C:\windows\system32\cmd.exe /K "$(FULL_CURRENT_PATH)"

import numpy as np
import cv2
import os

import video

print " __      ___     _               _____ _    "
print " \ \    / (_)   | |             / ____| |   "
print "  \ \  / / _  __| | ___  ___   | |  __| | __ _ ___ ___  ___  ___  "
print "   \ \/ / | |/ _` |/ _ \/ _ \  | | |_ | |/ _` / __/ __|/ _ \/ __| "
print "    \  /  | | (_| |  __/ (_) | | |__| | | (_| \__ \__ \  __/\__ \ "
print "     \/   |_|\__,_|\___|\___/   \_____|_|\__,_|___/___/\___||___/ "

print "\n ...for James"
print "\n Wash in the pool of Siloam"


global video_srcR, video_srcL
video_srcR = 0
video_srcL = 3

print "\n\n\n\n\n Right video source: camera # "+str(video_srcR)
print " Left video source: camera # "+str(video_srcL)

class App(object):
    def __init__(self, video_srcR, video_srcL):
		#self.camR = video.create_capture(video_srcR)
		self.camL = video.create_capture(video_srcL)
		#self.frameR = self.camR.read()
		self.frameL = self.camL.read()

		cv2.namedWindow('videobox')
		#cv2.namedWindow('edge')
		#cv2.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
		#cv2.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)


    def run(self):  #------------------------------------------------------

		showedge = 0
		edge_thrsh_1 = 1500
		edge_thrsh_2 = 2000

		while True:
			#ret, self.frameR = self.camR.read()       	# Nab a frame of video stream
			ret, self.frameL = self.camL.read()       	# Nab a frame of video stream

			#right_frame = self.frameR               		# Copy it to a numpy array/object thing
			left_frame = self.frameL

			right_frame = np.zeros_like(left_frame) 			# There is no left camera :-(


			#thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
			#thrs2 = cv2.getTrackbarPos('thrs2', 'edge')

			#right_frame = cv2.Canny(right_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)
			#left_frame = cv2.Canny(left_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)

			focal_length = 600; # i think this is the focal length of the lens, measured in pixels
			x_offset = 300;
			y_offset = 230;

			if(showedge):
				right_edge = cv2.Canny(right_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)
				left_edge = cv2.Canny(left_frame, edge_thrsh_1, edge_thrsh_2, apertureSize=5)

				right_frame[right_edge != 0] = (0,255,255)
				left_frame[left_edge != 0] = (0,255,255)

			#right_frame = np.split(right_frame, 2, axis=1)[0]
			#left_frame = np.split(left_frame, 2, axis=1)[0]

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

			right_frame = np.rot90(right_frame, 3)
			left_frame = np.rot90(left_frame, 1)

			#cv2.imshow('right_eye', right_frame)
			video_out = np.concatenate((left_frame, right_frame),axis=1)

			cv2.imshow('videobox', video_out)

			ch = 0xFF & cv2.waitKey(5)

			if ch == ord('e'):
				showedge = not showedge

		cv2.destroyAllWindows()


if __name__ == '__main__':
	import sys

	window_width = 1260;
	window_height = int((float(4/3) * float(window_width)));

	cv2.namedWindow('videobox', 2)

	cv2.resizeWindow('videobox', window_width, window_height)

	def nothing(*arg):
		pass

	cv2.moveWindow('videobox', 0, 0)

	App(video_srcR, video_srcL ).run()

