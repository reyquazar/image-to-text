import cv2

# Load the noisy document image
image_path = "test.png"  # Replace with your image path
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale for simplicity

if img is None:
    print(f"Error: Could not load image at {image_path}")
else:
    # Example: Apply Median Filter for salt-and-pepper noise
    # Kernel size (e.g., 3, 5, 7) should be an odd number
    denoised_median = cv2.medianBlur(img, 5)

    # Example: Apply Gaussian Filter for Gaussian noise
    # Kernel size (e.g., (5,5)) and standard deviation (e.g., 0)
    denoised_gaussian = cv2.GaussianBlur(img, (5, 5), 0)

    # Example: Apply Non-Local Means Denoising for more complex noise
    # h: filter strength, hColor: filter strength for color images (set to 0 for grayscale)
    # templateWindowSize, searchWindowSize: parameters for patch comparison
    denoised_nl_means = cv2.fastNlMeansDenoising(img, None, h=30, templateWindowSize=7, searchWindowSize=21)

    # Display or save the denoised images
    cv2.imshow("Original Image", img)
    cv2.imshow("Denoised (Median Filter)", denoised_median)
    cv2.imshow("Denoised (Gaussian Filter)", denoised_gaussian)
    cv2.imshow("Denoised (Non-Local Means)", denoised_nl_means)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # You can also save the denoised image
    # cv2.imwrite("denoised_document.png", denoised_nl_means)
