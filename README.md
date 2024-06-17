# Flood Solver

Solver for _flood_ game. Code is extracted from the quarto markdown file

```sh
quarto convert flood.qmd --output /dev/stdout --quiet \
  | jupyter nbconvert --to python --stdout --stdin --log-level 50 \
  | sed -e '/^---/,/^---/d' \
  | sed -e '/^#/d' | sponge flood.py

# reformat with black
black flood.py
```

