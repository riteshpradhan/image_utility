#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import Image


def convert(args):
    in_dir = os.path.abspath(str(args.idir))
    out_dir = os.path.abspath(str(args.odir))
    quality = int(args.q)
    prefix = args.prefix
    size = args.resize

    try:
        os.makedirs(out_dir)
    except OSError as e:
        print "\t%s: %s" % (repr(e), out_dir)

    for root, dirs, files in os.walk(in_dir):
        print "\t%s %s %s" % (root, dirs, files)
        for fname in files:
            try:
                im = Image.open(os.path.join(root, fname))
                if size:
                    im = im.resize(size, Image.ANTIALIAS)
            except Exception as e:
                print "\t\t%s: %s" % (repr(e), fname)
                continue

            final_out_dir = root.replace(in_dir, out_dir)

            if not os.path.exists(final_out_dir):
                try:
                    os.makedirs(final_out_dir)
                except OSError as e:
                    print "\t%s: %s" % (repr(e), final_out_dir)

            if prefix:
                outfile = open(
                    os.path.join(final_out_dir, prefix + fname), "wb")
            else:
                outfile = open(os.path.join(final_out_dir, fname), "wb")
            im.save(outfile, quality=quality)
            outfile.close()


def dimension2d(s):
    try:
        width, height = map(int, s.split(','))
        return width, height
    except:
        raise argparse.ArgumentTypeError("Resize must be width, height")


def main():
    usage = """Usage: python thumbnail_creator.py puzzle_dir  -h  //for help"""
    print usage
    print "Photo conversion started ..."
    parser = argparse.ArgumentParser(
        description="Convert image quality, crop etc.")
    parser.add_argument(
        '--idir', required=True, help="path of input directory")
    parser.add_argument(
        '--odir', required=True, help="path of output directory")
    parser.add_argument('-q', default=50, help="Converted image quality")
    parser.add_argument('--prefix', help="Output files prefix")
    parser.add_argument(
        '--resize', help="width, height of the resized image",
        dest="resize", type=dimension2d)

    args = parser.parse_args()

    # print args
    convert(args)


if __name__ == "__main__":
    main()
