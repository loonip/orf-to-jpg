import glob
import rawpy
import imageio
import os

PROGRESS_BAR_LENGTH = 50
OUTPUT_DIR = "jpeg-ed"
DEBUG = True

def main(path, export_path=OUTPUT_DIR):
    if DEBUG:
        print(f"Processing '{path}'.")

    if os.path.isdir(path):
        # Use glob to find all .ORF and .orf files, ignoring hidden files
        orf_filelist = [file for file in glob.glob(os.path.join(path, '*.[oO][rR][fF]')) if not os.path.basename(file).startswith('.')]
        print(f"Found {len(orf_filelist)} ORF files in '{path}'.")

        if len(orf_filelist) != 0:

            i = 1
            check_and_make_dir(export_path)
            for infile in orf_filelist:
                rawpy_process(infile)
                if i % 10 == 0 or i == len(orf_filelist):
                    progress_bar(i, len(orf_filelist), infile)
                i += 1
            print('\nDone.')
        else:
            print(f"Error: No '*.ORF' images found in '{path}'.")

    elif os.path.isfile(path):
        if path.endswith('.ORF') or path.endswith('.orf'):
            rawpy_process(path)
    else:
        print(f"Error: '{path}' not found.")

def progress_bar(progress, total, infile):
    percent = PROGRESS_BAR_LENGTH * (progress / float(total))
    bar = '█' * int(percent) + ' ' * int(PROGRESS_BAR_LENGTH - percent)
    print(f"\r{os.path.basename(infile)}|{bar}| {percent*2:.2f}% |{progress}/{total}",end="\r")

def rawpy_process(path, output_dir):
    try:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess(
                no_auto_bright=True, # do not apply auto brightness ( use camera white balance )
                use_camera_wb=True, # use camera white balance
                output_bps=8, # for jpeg
                no_auto_scale=True,
                output_color=rawpy.ColorSpace.sRGB,
                user_qual=100
            )
            output_filename = os.path.join(output_dir, os.path.basename(path)[:-4] + '.jpg')
            imageio.imwrite(output_filename, rgb)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def check_and_make_dir(path):

    if DEBUG:
        print(f"Checking if directory '{path}' exists.")

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")
        pass
    else:
        pass

if __name__ == '__main__':

    # get the input path and output path
    inputpath = input('Enter The path (relative path ok).\nIf left blank, will default to current directory: ')
    if inputpath == '':
        inputpath = '.' # Default to current directory

    outputpath = input('Enter the output path.\nIf left blank, will default to "jpeg-ed": ')
    if outputpath == '':
        outputpath = OUTPUT_DIR

    path = os.path.abspath(inputpath)
    print(f"Input Path: {path}")
    print(f"Output Path: {outputpath}")

    main(path, outputpath)
