import cv2
import numpy as np
import os

def detect_and_remove_text(image_path, output_path=None):
    """
    Detects and removes text from an image using morphological operations
    and inpainting techniques.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the output image (optional)
        
    Returns:
        Image with text removed
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Use morphological operations to identify text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.dilate(binary, kernel, iterations=3)
    binary = cv2.erode(binary, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a mask for text regions
    mask = np.zeros_like(gray)
    
    # Filter contours based on area and aspect ratio to identify text regions
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        aspect_ratio = w / float(h)
        
        # Text regions typically have specific characteristics
        if area > 100 and aspect_ratio > 0.1 and aspect_ratio < 10:
            cv2.drawContours(mask, [contour], -1, 255, -1)
    
    # Dilate the mask to include nearby regions
    mask = cv2.dilate(mask, kernel, iterations=3)
    
    # Inpaint the text regions
    result = cv2.inpaint(image, mask, 7, cv2.INPAINT_TELEA)
    
    # Apply denoising to smooth the result
    result = cv2.fastNlMeansDenoisingColored(result, None, 10, 10, 7, 21)
    
    # Save the result if output path is provided
    if output_path:
        cv2.imwrite(output_path, result)
        
    return result

if __name__ == "__main__":
    # Example usage
    import matplotlib.pyplot as plt
    
    input_image = "synchtex2.jpeg"  # Replace with your image containing text
    output_image = "sample_images/text_removed.jpg"
    
    # Check if the input file exists
    if not os.path.exists(input_image):
        print(f"Error: Image file {input_image} not found.")
        exit(1)
        
    # Process the image
    result = detect_and_remove_text(input_image, output_image)
    
    # Display the results
    original = cv2.imread(input_image)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(122)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title('Text Removed')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()