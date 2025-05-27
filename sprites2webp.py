#!/usr/bin/env python
import argparse, os, sys, subprocess
from pathlib import Path

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("input", type=str)
parser.add_argument("--fps", type=float, default=5.0, help="|")
args = parser.parse_args()

def webp_task(directory):
	output_file = "unnamed.webp"
	if len(directory) > 0:
		output_file = Path(directory).stem + ".webp"

	subprocess.run([
		"ffmpeg",
		"-v",
		"quiet",
		"-y",
		"-f",
		"image2",
		"-pattern_type",
		"glob",
		"-framerate",
		str(args.fps),
		"-i",
		os.path.join(directory, "*.png"),
		"-filter_complex",
		"[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse",
		"-loop",
		"0",
		output_file
	], stdout=subprocess.DEVNULL)

webp_task(args.input)

sys.exit()
