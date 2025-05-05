# Ghostlines Detector

A Python application that detects "ghostlines" from webcam video by tracking motion vectors based on changes in the image's center of mass.

## Overview

Ghostlines Detector analyzes your webcam feed in real-time to visualize motion through vectors that represent how the overall "mass" of the frame is shifting. The program:

1. Processes webcam input in either color or grayscale
2. Calculates each frame's center of mass (treating darker pixels as having higher "mass")
3. Detects points that change significantly between frames
4. Draws red vectors showing the direction of overall movement

This creates an interesting visual effect that tracks motion across the frame, with vectors growing from points of change and pointing in the direction of the overall movement.

## Requirements

- Python 3.6 or higher
- OpenCV (`opencv-python`)
- NumPy

## Installation

1. Ensure you have Python installed on your system
2. Install the required dependencies:

```bash
pip install opencv-python numpy
```

3. Clone this repository or download the script

## Usage

Run the script with Python:

```bash
python ghostlines_detector.py
```

### Controls

- **M key**: Toggle between color and grayscale modes
- **Q key**: Quit the application

## How It Works

1. **Center of Mass Calculation**: The program calculates the "center of mass" of each frame by treating darker pixels as having higher mass. This is done by inverting the grayscale image (so black = high mass, white = low mass) and using OpenCV's moments calculation.

2. **Change Detection**: The program identifies points that have changed significantly between consecutive frames by calculating the absolute difference and applying a threshold.

3. **Vector Visualization**: From the detected change points, the program samples a subset and draws vectors showing the direction of the overall movement (determined by the change in the center of mass).

## Customization

You can modify these parameters in the code to adjust the behavior:

- `sample_points`: Number of points to sample for drawing vectors (default: 50)
- `change_threshold`: Minimum pixel value change to consider as significant (default: 30)
- `vector_scale`: Scaling factor for vector length (default: 5.0)
- `vector_color`: Color of the motion vectors in BGR format (default: (0, 0, 255) for red)

## Example Applications

- Visual arts installations
- Motion studies
- Interactive exhibits
- Visual effects experimentation

## License

This project is available under the MIT License.

## Acknowledgments

The Ghostlines Detector was inspired by concepts from computer vision and motion tracking techniques used in interactive art installations.
