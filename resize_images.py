#Edited by DGM @lotify. Referral Credits: https://github.com/GotG/object_detection_demo_flow/blob/master/resize_images.py
import os
import glob
import cv2

if __name__ == "__main__":
    import argparse
    max_height = 1920
    max_width = 1920

    parser = argparse.ArgumentParser(
        description="Resize raw images to uniformed target size."
    )
    parser.add_argument(
        "--raw-dir",
        help="Directory path to raw images.",
        default="./data/raw",
        type=str,
    )
    parser.add_argument(
        "--save-dir",
        help="Directory path to save resized images.",
        default="./data/images",
        type=str,
    )
    parser.add_argument(
        "--ext", help="Raw image files extension to resize.", default="jpg", type=str
    )

    args = parser.parse_args()

    raw_dir = args.raw_dir
    save_dir = args.save_dir
    ext = args.ext


    fnames = glob.glob(os.path.join(raw_dir, "*/*.{}".format(ext)))
    os.makedirs(save_dir, exist_ok=True)
    ffnames = []

    for f in fnames:
        if not 'small' in f:
            ffnames.append(f)

    print(
        "{} files to resize from directory `{}` to ext:{}".format(
            len(ffnames), raw_dir, ext
        )
    )
    for fname in ffnames:
      print(".", end="", flush=True)
      img = cv2.imread(fname, cv2.IMREAD_UNCHANGED)
      height, width = img.shape[:2]


      # only shrink if img is bigger than required
      if max_height < height or max_width < width:
          # get scaling factor
          scaling_factor = max_height / float(height)
          if max_width/float(width) < scaling_factor:
              scaling_factor = max_width / float(width)
          # resize image
          img_small = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
      else:
          img_small = img

      new_fname = fname.split('.'+ext)[0]
      new_fname = new_fname + "_small." + ext
      small_fname = os.path.join(save_dir, new_fname)
      print(small_fname)

      cv2.imwrite(small_fname, img_small)

    print(
        "\nDone resizing {} files.\nSaved to directory: `{}`".format(
            len(ffnames), save_dir
        )
    )
