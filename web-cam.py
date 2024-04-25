import cv2
import easyocr

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
        
    # 
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image)

        # print the extracted text to the console
        for result in results:
             print(result[1])
    #
    # needs work to display the text on the image
      
    # Break the loop on 'q' key press
    elif key == ord('q'):    
        break

# When everything is done, release the capture and close the window
cam.release()
cv2.destroyAllWindows()