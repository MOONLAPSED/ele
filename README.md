# ele

> `pip install -e .` # install as module using pip

> python setup.py develop (adds 'ele', 'ele_source', and 'ele_main' to $PATH)

ele will sort and organize my `2023dir` of 'RLHF' files and 'notes' using NLP, a Ubuntu-22.04-LTS docker container, and a custom python app

the end result will be a >`rlhf.db`` object or, preferably, methodology to be used going forward in 2024


### 2023dir:
includes multimedia, duplicates, snippets, and oddballs. Generated using a hectic collection of tools and sources, most notably being **LogSeq** and `Obsidian`. The latter likley being the basis of `ele syntax`

### ele syntax
Given that a dilimiter within the ele RLHF arcitechture is `(dilimiter = "---")`, the ele syntax is as follows:
    
    dilimiter

    body

    dilimiter OR EOF OR <|im_end|> OR ... (logic tbd)

with `ele syntax` defining an `ele frame`

### ele frame
binary encoded pipe-ready and embedding-ready core data type - enforced using polymorphisim and ABC in the application code

