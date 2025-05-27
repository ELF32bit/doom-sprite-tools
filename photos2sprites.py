#!/usr/bin/env python
import argparse, os, glob, multiprocessing, subprocess
from pathlib import Path

def parse_args():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("input", type=str)
	parser.add_argument("--crop", type=str, default="w:h:0:0", help="|")
	parser.add_argument("--scale", type=str, default="-1:-1", help="|")
	parser.add_argument("--scale_algorithm", type=str, default="lanczos", help="|")
	parser.add_argument("--color", type=str, default='2b6426', help="|")
	parser.add_argument("--similarity", type=float, default=0.1, help="|")
	parser.add_argument("--blend", type=float, default=0.03, help="|")
	parser.add_argument("--contrast", type=float, default=1.0, help="|")
	parser.add_argument("--brightness", type=float, default=0.0, help="|")
	parser.add_argument("--saturation", type=float, default=1.0, help="|")
	parser.add_argument("--gamma", type=float, default=1.0, help="|")
	parser.add_argument("--gamma_r", type=float, default=1.0, help="|")
	parser.add_argument("--gamma_g", type=float, default=1.0, help="|")
	parser.add_argument("--gamma_b", type=float, default=1.0, help="|")
	parser.add_argument("--gamma_weight", type=float, default=1.0, help="|")
	parser.add_argument("--output", type=str, help="|")
	args = parser.parse_args()

	if args.output != None:
		try:
			os.mkdir(args.output)
		except FileExistsError:
			pass
		except Exception:
			print("Error: Bad output directory")
			quit()

	return args

def photo_filters(args):
	return f"\
	crop={args.crop.replace('w', 'in_w').replace('h', 'in_h')}, \
	chromakey={args.color}:{args.similarity}:{args.blend}, \
	premultiply=inplace=1, \
	scale={args.scale}, \
	eq=contrast={args.contrast}: \
	brightness={args.brightness}: \
	saturation={args.saturation}: \
	gamma={args.gamma}: \
	gamma_r={args.gamma_r}: \
	gamma_g={args.gamma_g}: \
	gamma_b={args.gamma_b}: \
	gamma_weight={args.gamma_weight}, \
	curves=preset=linear_contrast, \
	cas=strength=0.05"

def photo_task(file, filters, args):
	output_file = Path(file).stem + ".png"
	if args.output != None:
		output_file = os.path.join(args.output, output_file)

	subprocess.run([
		"ffmpeg",
		"-v",
		"quiet",
		"-y",
		"-i",
		file,
		"-vf",
		filters,
		"-sws_flags",
		args.scale_algorithm,
		output_file
	], stdout=subprocess.DEVNULL)

if __name__ == '__main__':
	args = parse_args()
	photo_filters = photo_filters(args)

	photos = []
	for photo in glob.glob(args.input):
		if not photo.endswith(tuple([".png", ".PNG"])):
			photos.append(tuple([photo, photo_filters, args]))

	thread_pool = multiprocessing.Pool()
	thread_pool.starmap(photo_task, photos)
	thread_pool.close()