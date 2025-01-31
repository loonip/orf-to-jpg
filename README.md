[![Python application](https://github.com/loonip/orf-to-jpg/actions/workflows/python-app.yml/badge.svg)](https://github.com/loonip/orf-to-jpg/actions/workflows/python-app.yml)

# **ORF to JPEG Converter**
This Python script processes Olympus RAW (.ORF) image files by converting them to JPEG format. It scans a specified directory (or the current directory by default) for `.ORF` files and uses the `rawpy` library to process the images before saving them as `.jpg` files in a designated output directory (`jpeg-ed`).

fork from https://github.com/ayadseghairi/orf-to-jpg

### **Features**
- **Batch processing**: Converts multiple `.ORF` files in a directory at once.
- **Camera settings preservation**: Uses the camera's embedded settings (white balance, brightness, etc.) for accurate color representation.
- **Progress tracking**: Displays a progress bar to indicate the conversion status.
- **Directory handling**: Automatically creates the output directory if it does not exist.
- **Debugging mode**: Prints additional information for troubleshooting if `DEBUG = True`.

---

### **Installation**
Ensure you have the required dependencies installed:

```bash
pip install rawpy imageio
```

---

### **Usage**
1. Run the script:

   ```bash
   python main.py
   ```

2. Enter the path to the folder containing `.ORF` files or press **Enter** to process files in the current directory.

3. The converted JPEG files will be saved in the `jpeg-ed` folder.

---

### **Processing ORF Files with Camera Settings**
By default, the script applies the camera's white balance and prevents automatic brightness adjustments to ensure accurate color representation. The key function handling this is:

```python
def rawpy_process(path, output_dir):
    try:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess(
                use_camera_wb=True,  # Uses the camera's white balance
                no_auto_bright=True,  # Disables automatic brightness adjustment
                gamma=(1,1),  # Disables gamma correction for more accurate colors
                output_bps=8,  # Outputs 8-bit images for JPEG compatibility
                demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD  # Applies high-quality demosaicing
            )
            output_filename = os.path.join(output_dir, os.path.basename(path)[:-4] + '.jpg')
            imageio.imwrite(output_filename, rgb)
    except Exception as e:
        print(f"Error processing {path}: {e}")
```

These settings ensure that the JPEG output retains colors and brightness as close to the original photo as possible.
