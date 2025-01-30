import glob
import rawpy
import imageio
import os


def main():
    inputpath = input('Enter The path (relative path ok) : ')
    path = os.path.abspath(inputpath)
    output_dir = "jpeg-ed"

    if os.path.isdir(path):
        # Use glob to find all .ORF and .orf files, ignoring hidden files
        orf_filelist = [file for file in glob.glob(os.path.join(path, '*.[oO][rR][fF]')) if not os.path.basename(file).startswith('.')]

        if len(orf_filelist) != 0:
            check_and_make_dir(output_dir)

            i = 1
            for infile in orf_filelist:
                progress_bar(i, len(orf_filelist), infile)
                i += 1
                rawpy_prosess(infile)
            print('\nDone.')
        else:
            print(f"Error: No '*.ORF' images found in '{path}'.")

    elif os.path.isfile(path):
        if path.endswith('.ORF') or path.endswith('.orf'):
            check_and_make_dir(output_dir)
        rawpy_prosess(path)

    else:
        print(f"Error: '{path}' not found.")

def progress_bar(progress,total,infile):
    percent = 50 * (progress / float(total))
    bar = '█' * int(percent) + ' ' * int(50 - percent)
    print(f"\r{os.path.basename(infile)}|{bar}| {percent*2:.2f}% |{progress}/{total}",end="\r")

def rawpy_prosess(path):
    try:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
            nowfilename = os.path.join(output_dir, os.path.basename(path)[:-4] + '.jpg')
            imageio.imwrite(nowfilename, rgb)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")
    else:
        print(f"Directory '{path}' already exists.")

if __name__ == '__main__':
    main()
