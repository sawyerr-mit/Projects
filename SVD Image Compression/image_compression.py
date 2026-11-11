import numpy as np
import cv2
import os

# Run relative to this file so cat.jpg is found (and outputs are saved) next to the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Image Pre-Processing

img_path = "cat.jpg"
k = 40 # Compression Factor

img_bgr = cv2.imread(img_path)
b, g, r = cv2.split(img_bgr)
h, w = img_bgr.shape[:2]

blue_img = np.zeros((h,w,3), dtype='uint8')
blue_img[:,:,0] = b

green_img = np.zeros((h,w,3), dtype='uint8')
green_img[:,:,1] = g

red_img = np.zeros((h,w,3), dtype='uint8')
red_img[:,:,2] = r

cv2.imwrite("blue.jpg", blue_img)
cv2.imwrite("green.jpg", green_img)
cv2.imwrite("red.jpg", red_img)
cv2.imwrite("uncompressed.jpg", cv2.merge([b, g, r]))

# Image Compression Algorithm

def compress(arr, k):
    U, S, Vt = np.linalg.svd(arr, full_matrices=False)
    compressed_image = np.dot(U[:, :k], np.dot(np.diag(S[:k]), Vt[:k, :]))
    return np.clip(compressed_image, 0, 255).astype(np.uint8)

b_comp = compress(b, k)
g_comp = compress(g, k)
r_comp = compress(r, k)

blue_compressed = np.zeros((h,w,3), dtype='uint8')
blue_compressed[:,:,0] = b_comp

green_compressed = np.zeros((h,w,3), dtype='uint8')
green_compressed[:,:,1] = g_comp

red_compressed = np.zeros((h,w,3), dtype='uint8')
red_compressed[:,:,2] = r_comp

cv2.imwrite("blue_compressed.jpg", blue_compressed)
cv2.imwrite("green_compressed.jpg", green_compressed)
cv2.imwrite("red_compressed.jpg", red_compressed)
cv2.imwrite("compressed.jpg", cv2.merge([b_comp, g_comp, r_comp]))