import cv2
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style('whitegrid')
 
image = cv2.imread('sample_image3.png')
dst = cv2.fastNlMeansDenoisingColored(image, None, 11, 6, 7, 21)
 
row, col = 1, 2
fig, axs = plt.subplots(row, col, figsize=(15, 10))
fig.tight_layout()
axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0].set_title('Before')
axs[1].imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
axs[1].set_title('After')
plt.show()