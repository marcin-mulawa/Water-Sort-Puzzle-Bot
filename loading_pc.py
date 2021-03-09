import numpy as np
import cv2
import imutils

picture = 'puzzle.jpg'

def load_transform_img(picture):
    image = cv2.imread(picture)
    #image = imutils.resize(image, height=800)
    org = image.copy()
    #cv2.imshow('orginal', image)

    mask = np.zeros(image.shape[:2], dtype = "uint8")
    cv2.rectangle(mask, (680, 260), (1160, 910), 255, -1)
    #cv2.imshow("Mask", mask)

    image = cv2.bitwise_and(image, image, mask = mask)
    #cv2.imshow("Applying the Mask", image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('image', image)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edged = cv2.Canny(blurred, 140, 230)
    #cv2.imshow("Canny", edged)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print(len(cnts))

    cv2.fillPoly(edged, pts =cnts, color=(255,255,255))
    #cv2.imshow('filled', edged)

    fedged = cv2.Canny(edged, 140, 230) 
    #cv2.imshow("fedged", fedged)

    (cnts, _) = cv2.findContours(fedged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)


    # boxes = fedged.copy()
    # cv2.drawContours(boxes, cnts, 10, (100 , 200, 100), 2)
    # cv2.imshow("Boxes",  boxes)

    image = cv2.bitwise_and(org, org, mask = edged)
    #cv2.imshow("Applying the Mask2", image)

    puzzlelist = []
    boxes_positon = []
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)

        #print("Box #{}".format(i + 1))  
        box = org[y:y + h, x:x + w]
        boxes_positon.append( ( (x+x+w)/2, (y+y+h)/2 ) )
        cv2.imwrite(f'temp/box{i+1}.jpg',box)
        #cv2.imshow("Box", box)
        gray = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray", gray)
        mask = np.zeros(gray.shape[:2], dtype = "uint8")

        y1,y2 = 45, 60
        for i in range(4):
            cv2.rectangle(mask, (15, y1), (37, y2), 255, -1)
            y1,y2 = y1+45, y2+45
            
        #cv2.imshow("Mask2 ", mask)
        masked = cv2.bitwise_and(gray, gray, mask = mask)
        #cv2.imshow('Masked', masked)
        
        y1,y2 = 45, 60
        temp = []
        for i in range(4):
            value = masked[y1:y2,15:37]
            #cv2.imshow(f'val{i}',value)
            max_val = max(value.flatten())
            if max_val >= 45:
                temp.append(max_val)
            y1,y2 = y1+45, y2+45
        puzzlelist.append(temp[::-1])
        #cv2.waitKey(0)
    print(f'Pozycja początkowa: {puzzlelist[::-1]}\n')
    print(f'Pozycje boksow: {boxes_positon[::-1]}\n')
    return puzzlelist[::-1], boxes_positon[::-1], len(cnts)


if __name__ == '__main__':
    answer, boxes_positon[::-1], boxes = load_transform_img('level/screen.jpg')
    print(answer)
