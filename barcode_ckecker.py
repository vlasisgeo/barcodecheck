

import cv2
from pyzbar import pyzbar
from collections import defaultdict

# Initialize video capture object
cap = cv2.VideoCapture(0)

# Initialize dictionary to store barcode counts
barcode_counts = defaultdict(int)

# Initialize dictionary to store counts of objects with each barcode
object_counts = defaultdict(int)

# Initialize set to keep track of barcodes detected in previous frame
previous_barcodes = set()

while True:
    # Read frame from video capture object
    ret, frame = cap.read()

    # Convert frame to grayscale for barcode detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the frame
    barcodes = pyzbar.decode(gray)

    # Initialize set to keep track of barcodes detected in current frame
    current_barcodes = set()

    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # Check if barcode has not been detected before
        if barcode_data not in previous_barcodes:
            # Increment barcode count
            barcode_counts[barcode_data] += 1

        # Increment object count for barcode
        object_counts[barcode_data] += 1
        print(object_counts)

        # Draw barcode boundary box and text on the frame
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{barcode_data} ({barcode_type}): {object_counts[barcode_data]}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Add barcode to current_barcodes set
        current_barcodes.add(barcode_data)
        print(current_barcodes)

    # Update previous_barcodes set
    previous_barcodes = current_barcodes

    # Display the frame
    cv2.imshow('Barcode Detection', frame)

    # Check for user keypress to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release video capture object and close all windows
cap.release()
cv2.destroyAllWindows()

# Print barcode counts
for barcode_data, count in barcode_counts.items():
    print(f"Barcode '{barcode_data}' was detected {count} times with {object_counts[barcode_data]} objects.")