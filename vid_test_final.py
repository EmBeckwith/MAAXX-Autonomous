import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0) # start video capture. 0 is used as only one camera plugged in
out = cv2.VideoWriter('test2.avi', -1, 20.0, (640,480)) # Initialise variable for video output

t_end = time.time() + 60 *0.5 # Takes current time and adds 30 seconds (always seems to output 22-23 seconds for some reason)
while time.time() < t_end: # Goes until timer runs out

    ret, frame = cap.read() # Capture frame-by-frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,300,425,apertureSize = 5) # Canny edge detection. If aperture size is decreased, will need to lower thresholds in box 2 and 3
    lines = cv2.HoughLines(edges,1,np.pi/360,175) # Adjust transform in

    # Need to test more on curved shapes. Harder to adjust it so it only finds the line if the object is curved. Some compromise between apertureSize, and the three thresholds must be
    #found to gaurantee line detection
    if isinstance(lines, np.ndarray):
        rho_sum=lines[:,0,0].sum()
        theta_sum=lines[:,0,1].sum()
        n=len(lines)
        rho_av=rho_sum/n
        theta_av=theta_sum/n
        a = np.cos(theta_av)
        b = np.sin(theta_av)
        x0 = a*rho_av
        y0 = b*rho_av
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0-1000*(-b))
        y2 = int(y0-1000*(a))
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),10)
        print(theta_av)
        print(rho_av)
        if theta_av<-0.174533 or theta_av>0.174533: #Angle measured in radians
            print('Drone Not going straight on line')
        if rho_av<220 or rho_av>420:                #Took Approximate Values. Centre approximately around 320
            print('Drone not centred on line')
        cv2.imshow('frame',frame)
        out.write(frame)
    else:
        cv2.imshow('frame',gray)
        out.write(gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
