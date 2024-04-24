import cv2

# Open the webcam (0 for default camera, 1 for the second camera, etc.)
cam = cv2.VideoCapture(0)

result, image = cam.read()

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and close the window
cam.release()
cv2.destroyAllWindows()