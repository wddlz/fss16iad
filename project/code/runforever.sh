#!/bin/bash
for i in {1..100}; do
  echo -e "\nROUND $i\n"
  for j in {1..10}; do
    python -m scoop -n 20 run.py
  done
done 2>/dev/null
