import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

t_end = time.time() + 60 *0.5
out = cv2.VideoWriter('test2.avi', -1, 20.0, (640,480))

while time.time() < t_end:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,300,425,apertureSize = 5)
    #
    lines = cv2.HoughLines(edges,1,np.pi/60,175)
    i=0
    # #img2=cv2.imwrite('edges5.jpg',edges)
    rho_sum=0
    theta_sum=0
    if isinstance(lines, np.ndarray):
        while i<len(lines):
            for rho,theta in lines[i]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0+1000*(-b))
                y1 = int(y0+1000*(a))
                x2 = int(x0-1000*(-b))
                y2 = int(y0-1000*(a))
                rho_sum=rho+rho_sum
                theta_sum=theta+theta_sum
                    #cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                i=i+1
        rho_av=rho_sum/i
        theta_av=theta_sum/i
        a = np.cos(theta_av)
        b = np.sin(theta_av)
        x0 = a*rho_av
        y0 = b*rho_av
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0-1000*(-b))
        y2 = int(y0-1000*(a))
        cv2.line(edges,(x1,y1),(x2,y2),(255,0,0),10)
            #print('finished')
            #print(i)
            #print(rho_sum)
            #print(theta_sum)
        print(theta_av)
        print(rho_av)
        cv2.imshow('frame',edges)
        out.write(edges)
    else:
        cv2.imshow('frame',edges)
        out.write(edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
