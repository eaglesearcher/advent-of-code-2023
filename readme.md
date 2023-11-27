# Advent of Code 2023 🎄

Python solutions to AOC 23.

[AOC 2022](https://github.com/eaglesearcher/advent-of-code-2022)

# Running solutions

Each day{#}.py is self-contained.
Run `python day#.py`

# Cloning

`file_io.py` creates new days and automates data pulling.

`file_io.new_day(#)` -> spawns a new day#.py file by copying the dayX.py template and updating the day#.

`file_io.read_input(#)` -> grabs input files from `./input/`
If the file is not found, automatically attempts to pull and create the file `file_io.pull_data()`

For automated pulling, update `AOC_YEAR` at the top of `file_io.py` for the current year.

# Secret Sauce

`algo_util.py` holds commonly reused algo components, but since it is in development throughout the course of the event, the latest is not guarenteed to work with earlier daily solutions (but I try).

# Examples

See `scratch.py` for file_io tests and basic daily solution timing.

# Compatibility

Primarily development in core python with sprinkles of numpy.
AOC 23 environment:
python 3.11.5
numpy 1.24.3