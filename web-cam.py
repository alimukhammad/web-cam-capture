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

        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            print(f"Error converting image to grayscale: {e}")

        # Blur the image

        try:
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
        except Exception as e:
            print(f"Error applying blur detection: {e}")

        try:
            edges = cv2.Canny(blur, 50, 200)
        except Exception as e:
            print(f"Error applying Canny edge detection: {e}")

        # Find contours in the edged image
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1]

        reader = easyocr.Reader(['en'])

        # print the extracted text to the console
        try:
            results = reader.readtext(image)
            for result in results:
                print(result[1])
        except Exception as e:
            print(f"Error reading text from image: {e}")
      
        # Break the loop on 'q' key press
        if cv2.waitKey(10) == ord('q'):    
            break

# When everything is done, release the capture and close the window
cam.release()
cv2.destroyAllWindows()