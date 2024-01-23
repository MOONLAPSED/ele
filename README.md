# ele

> `pip install -e .` # Install as a module using pip

> `python setup.py develop` (adds 'ele', 'ele_source', and 'ele_main' to $PATH)

Ele is designed to sort and organize my `2023dir` of 'RLHF' files and notes using NLP, an Ubuntu-22.04-LTS docker container, and a custom Python app.

The end result will be a `rlhf.db` object or, preferably, a methodology to be used going forward in 2024.

## 2023dir:
Includes multimedia, duplicates, snippets, and oddballs. Generated using a hectic collection of tools and sources, most notably being **LogSeq** and `Obsidian`. The latter likely being the basis of `ele syntax`.

## Ele Syntax
Given that a delimiter within the ele RLHF architecture is `(delimiter = "---")`, the ele syntax is as follows:

    delimiter

    body

    delimiter OR EOF OR ... (logic to be determined)

With `ele syntax` defining an `ele frame`.

## Ele Frame
Binary encoded, pipe-ready, and embedding-ready core data type - enforced using polymorphism and ABC in the application code.
