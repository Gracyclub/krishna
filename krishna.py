import cv2
import numpy as np


img = cv2.imread("krishna.jpg")
if img is None:
    print("image not found! please check 'krishna.jpg' ")
    exit()

height, width = img.shape[:2]
window_name = "Krishna Neon Art Animation"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, width, height)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

all_points = []
for cnt in contours:
    for pt in cnt:
        all_points.append(pt[0])

canvas = np.zeros((height, width, 3), dtype=np.uint8)
speed = 25  

for i in range(0, len(all_points), speed):
    batch = all_points[i:i + speed]
    for x, y in batch:
        color = [int(c) for c in img[y, x]]
        cv2.circle(canvas, (x, y), 1, color, -1)

    glow = cv2.GaussianBlur(canvas, (15, 15), 0)
    frame = cv2.addWeighted(canvas, 1.2, glow, 1.4, 0)

    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


center = (width // 2, height // 2)


for angle in range(0, 360, 6):
    rot_mat = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    rotated = cv2.warpAffine(img, rot_mat, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

    
    glow = cv2.GaussianBlur(rotated, (15, 15), 0)
    frame = cv2.addWeighted(rotated, 1.1, glow, 1.2, 0)

    cv2.imshow(window_name, frame)
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break


for _ in range(3):
    
    for scale in np.linspace(1.0, 1.15, 20):
        mat = cv2.getRotationMatrix2D(center, 0, scale)
        zoomed = cv2.warpAffine(img, mat, (width, height))
        
        glow = cv2.GaussianBlur(zoomed, (25, 25), 0)
        frame = cv2.addWeighted(zoomed, 1.2, glow, 1.5, 0)
        
        cv2.imshow(window_name, frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

   
    for scale in np.linspace(1.15, 1.0, 20):
        mat = cv2.getRotationMatrix2D(center, 0, scale)
        zoomed = cv2.warpAffine(img, mat, (width, height))
        
        glow = cv2.GaussianBlur(zoomed, (15, 15), 0)
        frame = cv2.addWeighted(zoomed, 1.2, glow, 1.0, 0)
        
        cv2.imshow(window_name, frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break


cv2.imshow(window_name, img)
cv2.waitKey(0)
cv2.destroyAllWindows()