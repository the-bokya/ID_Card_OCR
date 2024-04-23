import cv2
import matplotlib.pyplot as plt
import numpy as np

im = cv2.imread("cap.jpg")
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
plt.subplot(1, 2, 1)
plt.imshow(im, "gray")
blurred = cv2.GaussianBlur(im, (11, 11), 7.0)
im = np.clip((im - 0.4 * blurred) * 1.5, 0, 255).astype("uint8")
im = np.clip(np.power(im, 1.4) // (5), 0, 255)
plt.subplot(1, 2, 2)
plt.imshow(im, "gray")

plt.show()
