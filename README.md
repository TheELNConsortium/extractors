# Extractors
Find a common way to extract metadata and thumbnails from research data files

## Design
### Goals
- common interface into and out-of the extractor
- low entrance barrier to writing extractors to allow scientist to
  - change the present ones
  - write their own
  - share with friends and team
- allow for different path through the extractor
  - different 'recipes'
- since things are standardized, one can parse them
  - similar to 'pylint' parsing the source to identify problems

### Decisions following from low entrance barrier
- use json / dictionaries for interfacing but not json-ld (use schema.org terminology though)
- examples do not use try-except (it can be used by advanced users)
- no failsafes or checks in extractors (input and output should verify itself)

## Table of content
- example implementations in python
- example data files
- testExtractor.py, an example implementation of how a wrapper for all extractors could look like

### Examples
```
./testExtractor.py DataFiles/simple.png
./testExtractor.py DataFiles/simple.png image/crop
./testExtractor.py DataFiles/simple.csv
./testExtractor.py DataFiles/simple.csv red
```

