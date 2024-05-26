import cv2
import easyocr
import numpy as np

# Open the webcam (0 for default camera, 1 for the second camera, etc.)
cam = cv2.VideoCapture(0)

frame_counter = 0
result, image = cam.read()

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Wait for a key press for 1 millisecond
    key = cv2.waitKey(1) & 0xFF

    # Save the frame on 'c' key press
    if key == ord('c'):
        # save image to variable
        image = frame.copy()

        cv2.imwrite('frame_{}.png'.format(frame_counter), frame)
        frame_counter += 1

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur the image
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Find edges in the image
        edged = cv2.Canny(blur, 50, 200)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1]

        # Get the contour of the document
        screenCnt = None
        for c in contours:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our document
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is not None:
            # Apply perspective transform
            pts = screenCnt.reshape(4, 2)
            rect = np.zeros((4, 2), dtype = "float32")

            # the top-left point has the smallest sum whereas the
            # bottom-right has the largest sum
            s = pts.sum(axis = 1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # compute the difference between the points -- the top-right
            # will have the minumum difference and the bottom-left will
            # have the maximum difference
            diff = np.diff(pts, axis = 1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # multiply the rectangle by the original ratio
            rect *= 1

            # now that we have our rectangle of points, let's compute
            # the width of our new image
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

            # ...and now for the height of our new image
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            # take the maximum of the width and height values to reach
            # our final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))

            # construct our destination points which will be used to
            # map the screen to a top-down, "birds eye" view
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype = "float32")

            # calculate the perspective transform matrix and warp
            # the perspective to grab the screen
            M = cv2.getPerspectiveTransform(rect, dst)
            warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

            # we could use this `warp` image and feed to our OCR reader

        reader = easyocr.Reader(['en'])
        results = reader.readtext(image)

        # print the extracted text to the console
        for result in results:
            print(result[1])
      
    # Break the loop on 'q' key press
    elif key == ord('q'):    
        break

# When everything is done, release the capture and close the window
cam.release()
cv2.destroyAllWindows()