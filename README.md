[![Documentation](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/build_docs.yml/badge.svg)](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/build_docs.yml) [![Testing](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/test.yml/badge.svg)](https://github.com/SiebeLeDe/pyfrag_plot/actions/workflows/test.yml)


# PyFrag Plotter

Scripts for plotting pyfrag calculations using the input and text files created by [PyFrag](https://pyfragdocument.readthedocs.io/en/latest/install.html)

First clone the github page and move to the directory. Then install it locally in your python environment with
``pip install -e .``

## Docs

Link to the documentation: https://siebelede.github.io/pyfrag_plot/

## PyFrag inputfile order

Code that analyzes and plots data from pyfrag calculations

> [!IMPORTANT]
> Make sure that the order of the keys involving overlap, orbitalenergy and population are in the same order

### Overlap order

Order occupied / unoccupied does not matter, only the pairs are grouped together in the overlap & population keys

overlap A frag1 24 A frag2 9  
overlap A frag1 25 A frag2 9  
overlap A frag1 26 A frag2 8  

### Orbital energy order

Always in the order occupied - unoccupied

orbitalenergy A frag1 24  
orbitalenergy A frag2 9  
orbitalenergy A frag1 25  
orbitalenergy A frag2 9  
orbitalenergy A frag2 8  
orbitalenergy A frag1 26  

### Population order

Always in the order occupied - unoccupied

population A frag1 24  
population A frag2 9  
population A frag1 25  
population A frag2 9  
population A frag2 8  
population A frag1 26  

<!-- (Purpose)

Authors
Siebe & Simone

License (ook LICENSE file toevoegen)
MIT License

Recommended citation
https://coderefinery.github.io/social-coding/software-citation/ 
[Author], [Author], [Title], [Jaartal] etc. 

Copy-paste-able example to get started
Opties: 
- Linken 
- Code integreren

Dependencies and their versions or version ranges

Installation instructions

Tutorials covering key functionality

Reference documentation (e.g. API) covering all functionality

How do you want to be asked questions (mailing list or forum or chat or issue tracker)

Possibly a FAQ section

Contribution guide -->
