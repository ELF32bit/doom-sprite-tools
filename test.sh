#!/bin/bash

python photos2sprites.py \
	"examples/photos/*.jpg" \
	--color "2b6426" \
	--similarity 0.05 \
	--crop "2000:2000:500:0" \
	--scale "256:256" \
	--gamma_g 0.95 \
	--output "test-photos"

python sprites2webp.py \
	"test-photos" \
	--fps 5.0

python video2sprites.py \
	"examples/video.mp4" \
	--seek 2.0 \
	--duration 4.0 \
	--fps 2.0 \
	--color "2b6426" \
	--similarity 0.05 \
	--crop "1080:1080:250:0" \
	--scale "256:256" \
	--gamma_g 0.95 \
	--output "test-video"

python sprites2webp.py \
	"test-video" \
	--fps 5.0
