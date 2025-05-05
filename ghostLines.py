import cv2
import numpy as np
import random

def find_center_of_mass(frame):
    """Calculate the center of mass of a grayscale frame (black=high mass, white=low)"""
    # Invert frame so black (0) = high mass and white (255) = low mass
    inverted = 255 - frame
    
    # Calculate moments
    M = cv2.moments(inverted)
    
    # Calculate center of mass (centroid)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = frame.shape[1] // 2, frame.shape[0] // 2  # Default to center if no mass detected
        
    return (cX, cY)

def detect_ghostlines():
    """Main function to detect and visualize ghostlines"""
    # Access webcam
    cap = cv2.VideoCapture(0)
    
    # Check if webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set parameters
    sample_points = 50  # Number of points to sample for drawing vectors
    change_threshold = 30  # Minimum pixel value change to consider significant
    vector_scale = 5.0  # Scale factor to make vectors bigger
    vector_color = (0, 0, 255)  # Red color for all vectors (BGR format)
    
    # Initialize display mode (True for color, False for grayscale)
    color_mode = True
    
    # Initialize variables
    ret, prev_frame = cap.read()
    if not ret:
        print("Failed to grab first frame")
        return
        
    # Convert to grayscale for processing
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_center = find_center_of_mass(prev_gray)
    
    print("Press 'm' to toggle between color and grayscale mode")
    print("Press 'q' to quit")
    
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            break
            
        # Create a copy for drawing
        display_frame = frame.copy()
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Find center of mass for current frame
        center = find_center_of_mass(gray)
        
        # Calculate absolute difference between frames
        diff = cv2.absdiff(prev_gray, gray)
        
        # Find points where change is above threshold
        change_mask = diff > change_threshold
        change_points = np.where(change_mask)
        
        # If we have change points, sample some of them
        if len(change_points[0]) > 0:
            # Calculate how many points to sample (either sample_points or less if fewer points available)
            num_to_sample = min(sample_points, len(change_points[0]))
            
            # Randomly select indices
            if num_to_sample > 0:
                indices = random.sample(range(len(change_points[0])), num_to_sample)
                
                # Draw vectors from change points to direction of center of mass movement
                center_movement = (center[0] - prev_center[0], center[1] - prev_center[1])
                
                for idx in indices:
                    y, x = change_points[0][idx], change_points[1][idx]
                    
                    # Draw circles at change points
                    cv2.circle(display_frame, (x, y), 2, (0, 255, 0), -1)
                    
                    # Draw vectors (from change point in direction of center movement)
                    # Scale the vector to make it bigger
                    end_x = x + center_movement[0] * vector_scale
                    end_y = y + center_movement[1] * vector_scale
                    cv2.arrowedLine(display_frame, (x, y), (int(end_x), int(end_y)), vector_color, 2)
        
        # Display info text
        cv2.putText(display_frame, f"Movement: ({center[0] - prev_center[0]}, {center[1] - prev_center[1]})", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(display_frame, f"Mode: {'Color' if color_mode else 'Grayscale'}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Choose display based on mode
        final_display = display_frame if color_mode else cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
        
        # If in grayscale mode, convert back to BGR for consistent display
        if not color_mode:
            final_display = cv2.cvtColor(final_display, cv2.COLOR_GRAY2BGR)
        
        # Show frame
        cv2.imshow('Ghostlines Detector', final_display)
        
        # Update previous frame and center
        prev_gray = gray.copy()
        prev_center = center
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            # Toggle display mode
            color_mode = not color_mode
            print(f"Switched to {'color' if color_mode else 'grayscale'} mode")
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_ghostlines()
