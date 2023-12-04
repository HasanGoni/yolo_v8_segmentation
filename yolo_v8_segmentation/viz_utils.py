# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_viz_utils.ipynb.

# %% auto 0
__all__ = ['get_name', 'overlay_mask', 'overlay_mask_border_on_image']

# %% ../nbs/02_viz_utils.ipynb 4
import cv2
from pathlib import Path
import numpy as np
from fastcore.all import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.ndimage import binary_dilation, binary_erosion

# %% ../nbs/02_viz_utils.ipynb 6
get_name = np.vectorize(lambda x: Path(x).name)

# %% ../nbs/02_viz_utils.ipynb 13
def overlay_mask(
        im_path, 
        msk_path, 
        overlay_clr=(0, 1, 0),
        scale=1,
        alpha=0.5,
        ):
    'Creaete a overlay image from image and mask'
    # Read the grayscale image
    gray_img = cv2.imread(f'{im_path}', cv2.IMREAD_GRAYSCALE)
    if gray_img is None:
        raise ValueError("Could not read the grayscale image")

    # Read the mask image
    mask_img = cv2.imread(f'{msk_path}', cv2.IMREAD_GRAYSCALE)
    mask_img = mask_img.astype(bool)
    if mask_img is None:
        raise ValueError("Could not read the mask image")

    # Check if dimensions of both images are the same
    if gray_img.shape != mask_img.shape:
        raise ValueError("Dimensions of grayscale image and mask do not match")

    # Convert image to 3 channels
    rgb_img = np.stack([gray_img]*3, axis=-1)/255
    fig, ax = plt.subplots()
    ax.imshow(rgb_img)

    clrd_overlay = np.zeros_like(rgb_img)
    clrd_overlay[mask_img]=overlay_clr
    ax.imshow(clrd_overlay, alpha=alpha)





# %% ../nbs/02_viz_utils.ipynb 15
def overlay_mask_border_on_image(im_path, msk_path, border_color=(0, 1, 0), border_width=1):
    """
    Overlays the border of a binary mask on a grayscale image and displays the result using matplotlib.
    
    Args:
    image (numpy.ndarray): Grayscale image.
    mask (numpy.ndarray): Binary mask of the same size as the image.
    border_color (tuple): RGB color for the mask border in the range [0, 1].
    border_width (int): Width of the border.
    
    Returns:
    None: The function displays a plot.
    """
    gray_img = cv2.imread(f'{im_path}', cv2.IMREAD_GRAYSCALE)
    if gray_img is None:
        raise ValueError("Could not read the grayscale image")

    # Read the mask image
    mask_img = cv2.imread(f'{msk_path}', cv2.IMREAD_GRAYSCALE)
    mask_img = mask_img.astype(bool)
    if mask_img is None:
        raise ValueError("Could not read the mask image")

    # Check if dimensions of both images are the same
    if gray_img.shape != mask_img.shape:
        raise ValueError("Dimensions of grayscale image and mask do not match")
    # Ensure the mask is boolean

    # Find the borders of the mask
    dilated_mask = binary_dilation(mask_img, iterations=border_width)
    eroded_mask = binary_erosion(mask_img, iterations=border_width)
    border = dilated_mask & ~eroded_mask

    # Convert grayscale image to RGB
    rgb_image = np.stack([gray_img]*3, axis=-1) / 255.0  # Normalize for matplotlib

    # Apply the colored border
    rgb_image[border] = border_color

    # Display the image using matplotlib
    plt.imshow(rgb_image, cmap='gray')
    plt.axis('off')  # Turn off axis numbers
    plt.show()

