import numpy as np
import cv2
import imutils

picture = 'puzzle.jpg'

def load_transform_img(picture):
    image = cv2.imread(picture)
    image = imutils.resize(image, height=800)
    org = image.copy()
    #cv2.imshow('orginal', image)

    mask = np.zeros(image.shape[:2], dtype = "uint8")
    cv2.rectangle(mask, (15, 150), (440, 700), 255, -1)
    #cv2.imshow("Mask", mask)

    image = cv2.bitwise_and(image, image, mask = mask)
    #cv2.imshow("Applying the Mask", image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('image', image)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edged = cv2.Canny(blurred, 140, 230)
    #cv2.imshow("Canny", edged)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(len(cnts))

    cv2.fillPoly(edged, pts =cnts, color=(255,255,255))
    #cv2.imshow('filled', edged)

    fedged = cv2.Canny(edged, 140, 230) 
    #cv2.imshow("fedged", fedged)

    (cnts, _) = cv2.findContours(fedged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)


    boxes = fedged.copy()
    #cv2.drawContours(boxes, cnts, 10, (100 , 200, 100), 2)
    #cv2.imshow("Boxes",  boxes)

    image = cv2.bitwise_and(org, org, mask = edged)
    #cv2.imshow("Applying the Mask2", image)

    puzzlelist = []
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)

        print("Box #{}".format(i + 1))  
        box = org[y:y + h, x:x + w]
        cv2.imwrite(f'temp/box{i+1}.jpg',box)
        #cv2.imshow("Box", box)
        gray = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray", gray)
        mask = np.zeros(gray.shape[:2], dtype = "uint8")

        y1,y2 = 35, 50
        for i in range(4):
            cv2.rectangle(mask, (15, y1), (37, y2), 255, -1)
            y1,y2 = y1+40, y2+40
            
        #cv2.imshow("Mask2 ", mask)
        masked = cv2.bitwise_and(gray, gray, mask = mask)
        
        y1,y2 = 35, 50
        temp = []
        for i in range(4):
            value = masked[y1:y2,15:37]
            #cv2.imshow(f'val{i}',value)
            max_val = max(value.flatten())
            if max_val >= 45:
                temp.append(max_val)
            y1,y2 = y1+40, y2+40
        puzzlelist.append(temp[::-1])
        #cv2.waitKey(0)
    return puzzlelist[::-1] , len(cnts)
