import cv2
import numpy as np

img = cv2.imread('Hough_transform_test.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 5)

lines = cv2.HoughLines(edges,1,np.pi/60,70)
i=0
img2=cv2.imwrite('edges.jpg',edges)
rho_sum=0
theta_sum=0
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
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
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
cv2.line(img,(x1,y1),(x2,y2),(255,0,0),10)
cv2.imwrite('houghlines8.jpg',img)
print('finished')
print(i)
print(rho_sum)
print(theta_sum)
print(theta_av)
print(rho_av)
