# Importing the OpenCV library
import cv2

# Reading the image using imread() function
image = cv2.imread('image.jpg')

# We are copying the original image,
# as it is an in-place operation.
output = image.copy()

# Using the rectangle() function to create a rectangle.
text = cv2.putText(output, 'Sardor great', (100, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (100, 0, 0), 2)

# # Resizing the images
# image_resized = cv2.resize(image, (800, 600))
# rectangle_resized = cv2.resize(rectangle, (800, 600))

# Displaying the image with rectangle
cv2.imshow("Image with Rectangle", text)
cv2.waitKey(0)


