import glob
import rawpy
import imageio
import os

PROGRESS_BAR_LENGTH = 50
OUTPUT_DIR = "jpeg-ed"

def main(path):
    if os.path.isdir(path):
        # Use glob to find all .ORF and .orf files, ignoring hidden files
        orf_filelist = [file for file in glob.glob(os.path.join(path, '*.[oO][rR][fF]')) if not os.path.basename(file).startswith('.')]

        if len(orf_filelist) != 0:

            i = 1
            for infile in orf_filelist:
                check_and_make_dir(OUTPUT_DIR)
                if i % 10 == 0 or i == len(orf_filelist):
                    progress_bar(i, len(orf_filelist), infile)
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

def rawpy_process(path):
    try:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
            output_filename = os.path.join(OUTPUT_DIR, os.path.basename(path)[:-4] + '.jpg')
            imageio.imwrite(output_filename, rgb)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        printf(f"Directory '{path}' created.")
        pass
    else:
        pass

if __name__ == '__main__':
    inputpath = input('Enter The path (relative path ok).\nIf left blank, will default to current directory: ')
    if inputpath == '':
        inputpath = '.' # Default to current directory
    path = os.path.abspath(inputpath)
    main(path)
