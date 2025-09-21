# oDEtector - Object Detection with DETR

A Python-based object detection tool using Facebook's DETR (DEtection TRansformer) model to detect and annotate objects in images. The tool processes all images in a folder, draws bounding boxes around detected objects, and provides comprehensive analysis reports.

## Features

- **Object Detection**: Uses Facebook's DETR-ResNet-50 model for accurate object detection
- **Visual Annotations**: Draws red bounding boxes around detected objects
- **Text Labels**: Shows object name and confidence percentage on each detection
- **Batch Processing**: Processes all images in a folder automatically
- **Comprehensive Reports**: Provides detailed analysis including:
  - Expected vs. detected objects comparison
  - Missing objects list
  - Unexpected objects found
  - Images with no detections
- **Output Management**: Saves annotated images to an output folder

## Expected Objects

The tool is configured to detect the following 38 object categories:
- airplane, banana, bench, bird, boat, bowl, broccoli, bus, car, cat
- chair, clock, couch, dining table, dog, elephant, fire hydrant, fork
- giraffe, handbag, horse, person, pizza, potted plant, remote, sheep
- traffic light, truck, zebra, leopard, robot, firearm, tank, tie
- tv, phone, cup, keyboard, mouse, chicken, squirrel, bed, pillow, parsley, knife

## Installation

### Prerequisites

- Python 3.7 or higher
- Windows 10/11, Linux (Ubuntu/Debian/CentOS), or macOS
- For Windows: Long path support enabled (see below)

### Step 1: Enable Long Path Support on Windows

**Important**: Windows has a default path length limit of 260 characters. To avoid issues with deep folder structures, enable long path support:

#### Method 1: Using Registry Editor (Recommended)

1. **Open Registry Editor**:
   - Press `Win + R`, type `regedit`, and press Enter
   - Click "Yes" when prompted by User Account Control

2. **Navigate to the correct key**:
   ```
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   ```

3. **Create or modify the LongPathsEnabled value**:
   - Right-click in the right panel
   - Select "New" → "DWORD (32-bit) Value"
   - Name it `LongPathsEnabled`
   - Double-click the new value
   - Set "Value data" to `1`
   - Click "OK"

4. **Restart your computer** for the changes to take effect

#### Method 2: Using PowerShell (Run as Administrator)

```powershell
# Open PowerShell as Administrator and run:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Then restart your computer.

#### Method 3: Using Group Policy (Windows 10 Pro/Enterprise)

1. Press `Win + R`, type `gpedit.msc`, and press Enter
2. Navigate to: `Computer Configuration` → `Administrative Templates` → `System` → `Filesystem`
3. Double-click "Enable Win32 long paths"
4. Select "Enabled" and click "OK"
5. Restart your computer

### Step 2: Install Python Dependencies

#### For Windows:
```bash
pip install torch torchvision
pip install transformers
pip install pillow
```

#### For Linux (Ubuntu/Debian):

**Option A: Virtual Environment (Recommended)**
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install python3-pip python3-dev python3-venv python3-full

# Create a virtual environment
python3 -m venv oDEtector_env

# Activate the virtual environment
source oDEtector_env/bin/activate

# Install Python packages in the virtual environment
pip install torch torchvision
pip install transformers
pip install pillow

# Note: Always activate the virtual environment before running the script
# source oDEtector_env/bin/activate
```

**Option B: System-wide Installation (Alternative)**
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install python3-pip python3-dev

# Install packages system-wide (may require --break-system-packages)
pip3 install --user torch torchvision transformers pillow

# Or if you get "externally managed environment" error:
pip3 install --break-system-packages torch torchvision transformers pillow
```

#### For Linux (CentOS/RHEL):
```bash
# Install system dependencies
sudo yum install python3-pip python3-devel

# Create a virtual environment
python3 -m venv oDEtector_env

# Activate the virtual environment
source oDEtector_env/bin/activate

# Install Python packages in the virtual environment
pip install torch torchvision
pip install transformers
pip install pillow
```

#### For macOS:
```bash
# Using pip
pip install torch torchvision
pip install transformers
pip install pillow

# Or using conda
conda install pytorch torchvision -c pytorch
conda install -c conda-forge transformers pillow
```

#### Install all at once (any platform):
```bash
pip install torch torchvision transformers pillow
```

### Step 3: Download the Project

1. Clone or download this repository
2. Place your images in the `images` folder
3. Run the script

### Quick Setup Script (Linux)

For convenience, you can use this one-liner to set up everything on Linux:

```bash
# Download and setup in one command
git clone <repository-url> oDEtector && cd oDEtector && python3 -m venv oDEtector_env && source oDEtector_env/bin/activate && pip install torch torchvision transformers pillow
```

Or create a setup script:

```bash
#!/bin/bash
# setup.sh - Quick setup script for Linux
echo "Setting up oDEtector..."

# Create virtual environment
python3 -m venv oDEtector_env
source oDEtector_env/bin/activate

# Install dependencies
pip install torch torchvision transformers pillow

echo "Setup complete! To run the script:"
echo "1. source oDEtector_env/bin/activate"
echo "2. python3 main.py"
```

## Usage

### Basic Usage

1. **Prepare your images**:
   - Place all images you want to process in the `images` folder
   - Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF (case insensitive)

2. **Run the detection**:
   ```bash
   # Windows
   python main.py
   
   # Linux/macOS (with virtual environment)
   source oDEtector_env/bin/activate  # Activate virtual environment first
   python3 main.py
   
   # Linux/macOS (without virtual environment - if installed system-wide)
   python3 main.py
   ```

3. **View results**:
   - Annotated images will be saved in the `output` folder
   - Console will show detailed processing information
   - Summary report will be displayed at the end

### Output Structure

```
project/
├── images/              # Input images folder
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── output/              # Generated annotated images
│   ├── annotated_image1.jpg
│   ├── annotated_image2.png
│   └── ...
└── main.py             # Main detection script
```

### Console Output Example

```
Loading DETR model...
Model loaded successfully!

Found 25 images to process

================================================================================
Processing image 1/25: IMG_0773.JPG
================================================================================
Detected objects:
  - person with confidence 0.95 at location [120.5, 80.2, 200.3, 300.1]
  - car with confidence 0.92 at location [50.1, 150.8, 180.5, 250.3]
  Saved annotated image: output/annotated_IMG_0773.JPG

================================================================================
PROCESSING SUMMARY
================================================================================
Total images processed: 25
Images with objects detected: 20
Images with no objects detected: 3
Images with errors: 2

Expected objects list:
  airplane, banana, bench, bird, boat, bowl, broccoli, bus, car, cat, chair, clock, couch, dining table, dog, elephant, fire hydrant, fork, giraffe, handbag, horse, person, pizza, potted plant, remote, sheep, traffic light, truck, zebra, leopard, robot, firearm, tank, tie, tv, phone, cup, keyboard, mouse, chicken, squirrel, bed, pillow, parsley, knife

Objects actually found: car, cat, dog, person, pizza

Missing objects: airplane, banana, bench, bird, boat, bowl, broccoli, bus, chair, clock, couch, dining table, elephant, fire hydrant, fork, giraffe, handbag, horse, potted plant, remote, sheep, traffic light, truck, zebra, leopard, robot, firearm, tank, tie, tv, phone, cup, keyboard, mouse, chicken, squirrel, bed, pillow, parsley, knife

Unexpected objects found: bicycle, laptop

Images with no objects detected: IMG_0794.JPG, IMG_3133.jpg, IMG_3151.jpg

================================================================================
Processing complete!
Annotated images saved to: output/
================================================================================
```

## Configuration

### Detection Threshold

The confidence threshold is set to 0.9 (90%). To modify this, edit line 71 in `main.py`:

```python
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
```

Change `0.9` to your desired threshold (0.0 to 1.0).

### Expected Objects List

To modify the list of expected objects, edit the `expected_objects` list in `main.py` (lines 35-40).

## Troubleshooting

### Common Issues

1. **"Path too long" error (Windows only)**:
   - Ensure long path support is enabled (see installation step 1)
   - Restart your computer after enabling long path support

2. **CUDA out of memory**:
   - The script uses CPU by default
   - If you have CUDA and want to use GPU, modify the code to move tensors to GPU

3. **Font not found warning**:
   - The script will fall back to default font if system fonts are not available
   - This doesn't affect functionality, only text appearance
   - On Linux, install fonts: `sudo apt install fonts-dejavu-core` (Ubuntu/Debian)

4. **No objects detected**:
   - Check if your images contain the expected object types
   - Try lowering the confidence threshold
   - Ensure images are in RGB format (the script converts automatically)

5. **Permission denied errors (Linux)**:
   - Ensure you have write permissions in the project directory
   - Use `chmod +x main.py` if needed
   - Check that the output folder can be created

6. **Python not found (Linux)**:
   - Use `python3` instead of `python`
   - Install Python 3: `sudo apt install python3` (Ubuntu/Debian)
   - Check Python version: `python3 --version`

7. **"This environment is externally managed" error (Linux)**:
   - This is a new protection in modern Linux distributions
   - **Solution A**: Use a virtual environment (recommended)
   ```bash
   # Create and activate virtual environment
   python3 -m venv oDEtector_env
   source oDEtector_env/bin/activate
   pip install torch torchvision transformers pillow
   ```
   - **Solution B**: Use --user flag for user-level installation
   ```bash
   pip3 install --user torch torchvision transformers pillow
   ```
   - **Solution C**: Override the protection (use with caution)
   ```bash
   pip3 install --break-system-packages torch torchvision transformers pillow
   ```
   - **Solution D**: Use pipx for isolated installations
   ```bash
   sudo apt install pipx
   pipx install --include-deps torch transformers pillow
   ```

### Performance Tips

- **Batch Processing**: The script processes images sequentially for memory efficiency
- **Memory Usage**: Each image is processed individually to minimize memory usage
- **Large Images**: Very large images may take longer to process

## Model Information

- **Model**: facebook/detr-resnet-50
- **Architecture**: DETR (DEtection TRansformer)
- **Backbone**: ResNet-50
- **Dataset**: COCO 2017
- **Classes**: 91 object categories

## Requirements

- Python 3.7+
- PyTorch
- Transformers library
- Pillow (PIL)
- **Windows**: Windows 10/11 with long path support
- **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 7+, or similar
- **macOS**: macOS 10.14+ (Mojave or later)

## License

This project uses the DETR model from Facebook Research, which is available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify that long path support is enabled on Windows
4. Check that your images are in supported formats
