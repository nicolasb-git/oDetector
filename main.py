from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image, ImageDraw, ImageFont
import os
import glob
import platform

def get_font():
    """Get appropriate font for the current platform"""
    try:
        system = platform.system().lower()
        if system == "windows":
            # Try common Windows fonts
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/verdana.ttf"
            ]
        elif system == "linux":
            # Try common Linux fonts
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
                "/System/Library/Fonts/Arial.ttf"  # macOS fallback
            ]
        else:  # macOS or other
            font_paths = [
                "/System/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial.ttf"
            ]
        
        # Try each font path
        for font_path in font_paths:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, 16)
        
        # If no system font found, try to load default
        return ImageFont.load_default()
        
    except Exception:
        # Fallback to None if all else fails
        return None

# Load the model and processor once (more efficient)
print("Loading DETR model...")
print(f"Running on: {platform.system()} {platform.release()}")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
print("Model loaded successfully!\n")

# Get all image files from the images folder
images_folder = "images"
output_folder = "output"
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff', '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.GIF', '*.TIFF']
image_files = []

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created output folder: {output_folder}")

for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(images_folder, ext)))

# Remove duplicates and sort the files for consistent processing order
image_files = list(set(image_files))
image_files.sort()

print(f"Found {len(image_files)} images to process\n")

# Track results for summary
results_summary = []
images_with_objects = []
images_without_objects = []
images_with_errors = []
all_detected_objects = set()  # Track unique objects found across all images

# Expected objects list
expected_objects = [
    "airplane", "banana", "bench", "bird", "boat", "bowl", "broccoli", "bus", "car", "cat", 
    "chair", "clock", "couch", "dining table", "dog", "elephant", "fire hydrant", "fork", 
    "giraffe", "handbag", "horse", "person", "pizza", "potted plant", "remote", "sheep", 
    "traffic light", "truck", "zebra", "leopard", "robot", "firearm", "tank", "tie", "tv", "phone", "cup", "keyboard", "mouse", "chicken", "squirrel",
    "bed", "pillow", "parsley", "knife"
]

# Process each image
for i, image_path in enumerate(image_files):
    image_name = os.path.basename(image_path)
    
    # Print separator and image name
    print("=" * 80)
    print(f"Processing image {i+1}/{len(image_files)}: {image_name}")
    print("=" * 80)
    
    try:
        # Load and process the image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary (some images might be in different color modes)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        
        # Convert outputs (bounding boxes and class logits) to COCO API
        # let's only keep detections with score > 0.9
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
        
        # Print detected objects and draw bounding boxes
        if len(results["scores"]) > 0:
            print("Detected objects:")
            detected_objects = []
            
            # Create a copy of the image for drawing
            image_with_boxes = image.copy()
            draw = ImageDraw.Draw(image_with_boxes)
            
            # Get appropriate font for the current platform
            font = get_font()
            
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i, 2) for i in box.tolist()]
                object_name = model.config.id2label[label.item()]
                confidence = round(score.item(), 3)
                confidence_percent = round(confidence * 100, 1)
                print(f"  - {object_name} with confidence {confidence} at location {box}")
                detected_objects.append(f"{object_name} ({confidence})")
                # Add to unique objects set
                all_detected_objects.add(object_name)
                
                # Draw red bounding box
                # box format: [x1, y1, x2, y2] (top-left and bottom-right coordinates)
                draw.rectangle(box, outline="red", width=3)
                
                # Create label text
                label_text = f"{object_name} {confidence_percent}%"
                
                # Get text size for background rectangle
                if font:
                    bbox = draw.textbbox((0, 0), label_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                else:
                    text_width = len(label_text) * 6  # Approximate width
                    text_height = 12  # Approximate height
                
                # Position label above the bounding box
                label_x = box[0]  # x1 coordinate
                label_y = max(0, box[1] - text_height - 5)  # Above the box, but not above image
                
                # Draw background rectangle for text
                text_bg = [label_x, label_y, label_x + text_width + 4, label_y + text_height + 2]
                draw.rectangle(text_bg, fill="red", outline="red")
                
                # Draw text
                if font:
                    draw.text((label_x + 2, label_y + 1), label_text, fill="white", font=font)
                else:
                    draw.text((label_x + 2, label_y + 1), label_text, fill="white")
            
            # Save the image with bounding boxes
            output_path = os.path.join(output_folder, f"annotated_{image_name}")
            image_with_boxes.save(output_path)
            print(f"  Saved annotated image: {output_path}")
            
            images_with_objects.append(image_name)
            results_summary.append(f"✓ {image_name}: {', '.join(detected_objects)}")
        else:
            print("❌ No objects detected with confidence > 0.9")
            # Still save the original image to output folder
            output_path = os.path.join(output_folder, f"no_objects_{image_name}")
            image.save(output_path)
            print(f"  Saved image (no objects): {output_path}")
            
            images_without_objects.append(image_name)
            results_summary.append(f"❌ {image_name}: No objects detected")
            
    except Exception as e:
        print(f"❌ Error processing {image_name}: {str(e)}")
        images_with_errors.append(image_name)
        results_summary.append(f"❌ {image_name}: Error - {str(e)}")
    
    print()  # Add blank line between images

# Print summary as the final entry
print("=" * 80)
print("PROCESSING SUMMARY")
print("=" * 80)
print(f"Total images processed: {len(image_files)}")
print(f"Images with objects detected: {len(images_with_objects)}")
print(f"Images with no objects detected: {len(images_without_objects)}")
print(f"Images with errors: {len(images_with_errors)}")
print()

if images_without_objects:
    print("Images with no objects detected:")
    for image_name in images_without_objects:
        print(f"  - {image_name}")
    print()

if images_with_errors:
    print("Images with errors:")
    for image_name in images_with_errors:
        print(f"  - {image_name}")
    print()

print("Detailed Results:")
for result in results_summary:
    print(f"  {result}")

print()
# Show expected objects and which ones were found/missing
print("Expected objects list:")
expected_list = ", ".join(expected_objects)
print(f"  {expected_list}")
print()

if all_detected_objects:
    sorted_objects = sorted(list(all_detected_objects))
    objects_list = ", ".join(sorted_objects)
    print(f"Objects actually found: {objects_list}")
    
    # Find missing objects (expected but not found)
    missing_objects = [obj for obj in expected_objects if obj not in all_detected_objects]
    if missing_objects:
        missing_list = ", ".join(sorted(missing_objects))
        print(f"Missing objects: {missing_list}")
    else:
        print("All expected objects were found!")
    
    # Find unexpected objects (found but not in expected list)
    unexpected_objects = [obj for obj in all_detected_objects if obj not in expected_objects]
    if unexpected_objects:
        unexpected_list = ", ".join(sorted(unexpected_objects))
        print(f"Unexpected objects found: {unexpected_list}")
    else:
        print("No unexpected objects were found.")
else:
    print("No objects were detected in any image.")
    missing_list = ", ".join(sorted(expected_objects))
    print(f"Missing objects: {missing_list}")

print()

# Show images with no objects detected
if images_without_objects:
    no_objects_list = ", ".join(images_without_objects)
    print(f"Images with no objects detected: {no_objects_list}")
    print()

print("=" * 80)
print("Processing complete!")
print(f"Annotated images saved to: {output_folder}/")
print("=" * 80)