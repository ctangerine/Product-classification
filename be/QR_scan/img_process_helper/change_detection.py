import cv2
import numpy as np 
'''
Using change detection to detect the change between two images, using these algorithms:
1. Convert to grayscale
2. GaussianBlur
3. Absdiff - Absolute difference between two images
4. Thresholding
5. Dilation
6. Find contours
7. Draw contours
'''

class ChangeDetection:
    def __init__(self, contour_area_threshold=800, diff_threshold=20):
        """
        Initialize the ChangeDetection without the original image.
        Args:
            contour_area_threshold (int): Minimum contour area to consider a change significant.
            diff_threshold (int): Threshold value to consider pixel differences as a change.
        """
        self.original_image = None
        self.contour_area_threshold = contour_area_threshold
        self.diff_threshold = diff_threshold

    async def set_original_image(self, original_image):
        """
        Set the original image to be used as a reference for change detection.
        Args:
            original_image (ndarray): The original image to be used as a reference.
        """
        if isinstance(original_image, bytes):
            original_image = np.frombuffer(original_image, np.uint8)
            original_image = cv2.imdecode(original_image, cv2.IMREAD_COLOR)
        self.original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        self.original_image = cv2.GaussianBlur(self.original_image, (5, 5), 0)

    async def process_frame(self, new_frame):
        """
        Process the new frame to detect changes compared to the original image.
        Args:
            new_frame (ndarray): The new frame to compare against the original image.
        
        Returns:
            processed_frame (ndarray): The processed frame with changes highlighted.
            significant_change (bool): True if significant change is detected, otherwise False.
        """
        processed_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        processed_frame = cv2.GaussianBlur(processed_frame, (5, 5), 0)
        diff = cv2.absdiff(self.original_image, processed_frame)
        _, thresh = cv2.threshold(diff, self.diff_threshold, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        significant_change = False
        for contour in contours:
            if cv2.contourArea(contour) >= self.contour_area_threshold:
                significant_change = True
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return processed_frame, significant_change

    async def detect_and_notify(self, new_frame):
        """
        Detect changes and notify the server if a significant change is detected.
        Args:
            new_frame (ndarray): The new frame to be analyzed.
        
        Returns:
            message (str): A message indicating whether to proceed with QR code detection.
        """
        # convert bytes data to numpy array if needed 
        if isinstance(new_frame, bytes):
            new_frame = np.frombuffer(new_frame, np.uint8)
            new_frame = cv2.imdecode(new_frame, cv2.IMREAD_COLOR)
        _, significant_change = await self.process_frame(new_frame)
        if significant_change:
            return True
        else:
            return False