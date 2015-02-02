#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import glob
import Image


qual = 75       # range from 1 to 95 (normal is 75)

THUMBNAIL_STRING = "_thumbnail"
THUMBNAIL_SIZE = 120, 120
thumbnail_image_pattern = "*/*/*%s.jpg" % (THUMBNAIL_STRING)
all_image_pattern = "*/*/*.jpg"


def thumbnail_exists(file, ext, all_images):
    return file + THUMBNAIL_STRING + ext in all_images


def create_thumbnail(required_images, all_images):
    for infile in required_images:
        file, ext = os.path.splitext(infile)
        if thumbnail_exists(file, ext, all_images):
            print "\t\tThumbnail for %s exists. Skipping ..." % (file)
            continue
        print "\t\tCreating thumbnail for %s." % (file)
        im = Image.open(infile)
        im.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        im.save(file + THUMBNAIL_STRING + ext, quality=int(qual))
        print "\t\tThumbnail creation completed."


def main():
    usage = """Usage: python thumbnail_creator.py puzzle_dir  -h  //for help"""
    print usage
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir', default="./puzzles", help="path to the puzzle pack")
    args = parser.parse_args()

    print "\tThe path to puzzle is : %s " % (args.dir)
    all_images = glob.glob(os.path.join(args.dir, all_image_pattern))
    thumbnail_images = glob.glob(
        os.path.join(args.dir, thumbnail_image_pattern))

    required_images = list(set(all_images) - set(thumbnail_images))
    print "\tChecking and creating thumbnails for : %s" % (required_images)
    create_thumbnail(required_images, all_images)


if __name__ == "__main__":
    main()
