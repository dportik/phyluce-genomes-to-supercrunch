# phyluce-genomes-to-supercrunch

---------------

## Overview

`phyluce-genomes-to-supercrunch.py` is a python script that can be used to
(i) combine the genome-extracted UCE sequences for multiple fasta files output by Phyluce,
and (ii) relabel the fasta records to a format that is similar to GenBank records.
This format is compatible with [SuperCRUNCH](https://github.com/dportik/SuperCRUNCH) and 
allows the UCE sequence data to be parsed into individual loci correctly. To work properly, 
the input fasta files from Phyluce should be labeled with the following format: `Genus_species.fasta`.

## Installation

`phyluce-genomes-to-supercrunch.py` is written in Python (2.7) and functions as a stand-alone 
command-line script. It can be downloaded and executed independently without the need to 
install any additional Python packages or libraries, making it easy to use and edit.

## License

GNU Lesser General Public License v3.0

## Explanation 

To make use of this script, you will first need to extract UCE sequences from genomes using Phyluce. 
Afterwards, you can use this script to reformat and relabel the output files to a fasta format compatible
with the bioinformatics toolkit SuperCRUNCH. SuperCRUNCH can then be used to parse all the sequences into 
unaligned UCE-specific fasta files, and subsequently filter and align sequences for each UCE locus.

In order to generate UCE sequences extracted from genomes, I followed the tutorial on the
PHYLUCE documentation called: [Tutorial III: Harvesting UCE Loci From Genomes](https://phyluce.readthedocs.io/en/latest/tutorial-three.html)

In brief, this involved:

1. Downloading genome assembly data in fasta format, then converting to 2bit format using `faToTwoBit`.

2. Using the genome assembly in 2bit format to generate a size information file (`sizes.tab`) using `twoBitInfo`.

3. Creating a directory structure of 2bit files and size files like so:

```
Inputs
│
├──Alligator_mississippiensis
│	├── Alligator_mississippiensis.2bit
│	└── sizes.tab
│
├──Chrysemys_picta
│	├── Chrysemys_picta.2bit
│	└── sizes.tab
│
├──Anolis_carolinensis
│	├── Anolis_carolinensis.2bit
│	└── sizes.tab
│
├──Gekko_japonicus
│	├── Gekko_japonicus.2bit
│	└── sizes.tab
```

4. Running `phyluce_probe_run_multiple_lastzs_sqlite` from Phyluce to generate an SQL database, using the `uce-5k-probes.fasta` file.

5. Running `phyluce_probe_slice_sequence_from_genomes` from Phyluce to extract UCE sequences into fasta files.

6. At the end, the output directory was populated with a relevant fasta file for each genome:

```
Outputs
│
├──Alligator_mississippiensis.fasta
│
├──Chrysemys_picta.fasta
│
├──Anolis_carolinensis.fasta
│
├──Gekko_japonicus.fasta
```

If you look inside the contents one of these output fasta files, the record descriptions have a lot
of extra information:

```
>Node_0_length_1119_cov_1000|contig:AKHW03001146.1|slice:26076133-26077252|uce:uce-502|match:26076632-26076752|orient:set(['+'])|probes:1
CATTATTAGAGAGCTCTTTCTagtaagcctttaaaaaaaaaaaaaaagaaaaaaaagaaa...

>Node_1_length_1120_cov_1000|contig:AKHW03000416.1|slice:16386850-16387970|uce:uce-507|match:16387350-16387470|orient:set(['+'])|probes:1
TGTAATGTATTTCATGTTTAGCACCTATTTATTCCATGTAACTTCACCATATCAAATGAG...

>Node_2361_length_1119_cov_1000|contig:AKHW03003826.1|slice:9139587-9140706|uce:uce-5821|match:9140087-9140206|orient:set(['+'])|probes:1
CAGTTGCAAGACAAACATGTATGGGAGGCAGAATGGGGAGGGAAATTAAACACATCAAGA...

>Node_2364_length_1121_cov_1000|contig:AKHW03000563.1|slice:14175404-14176525|uce:uce-4621|match:14175904-14176025|orient:set(['-'])|probes:1
TTAGTGATATAGTTGATCATTGAATTCTGTCTTCTATATTAAATTAGAAGAATGTTTAAA...
```

The goal of `phyluce-genomes-to-supercrunch.py` is to use this information to relabel the records
in a more useful way, and to combine records from multiple output fasta files to create a single
fasta file that is compatible with SuperCRUNCH. The format of the labeling is intended to mimic
what is typically present in NCBI GenBank records, which generally contain:

```
>[Accession] [taxon label] [remaining description line including gene information]
```

The general format of the description lines written by `phyluce-genomes-to-supercrunch.py` is:

```
>GENOME_[taxon].[uce-label] [taxon] genome ultra conserved element [uce-label]
```

Here, the `taxon` label will be the name of the output fasta file, and the `uce-label` will be pulled
from the description lines. So, let's say the input fasta file that contained the record labels above
is called `Gekko_japonicus.fasta`. The records above will be converted into the following:

```
>GENOME_Gekko_japonicus.uce-502 Gekko japonicus genome ultra conserved element uce-502
CATTATTAGAGAGCTCTTTCTAGTAAGCCTTTAAAAAAAAAAAAAAAGAAAAAAAAGAAA...

>GENOME_Gekko_japonicus.uce-507 Gekko japonicus genome ultra conserved element uce-507
TGTAATGTATTTCATGTTTAGCACCTATTTATTCCATGTAACTTCACCATATCAAATGAG...

>GENOME_Gekko_japonicus.uce-5821 Gekko japonicus genome ultra conserved element uce-5821
CAGTTGCAAGACAAACATGTATGGGAGGCAGAATGGGGAGGGAAATTAAACACATCAAGA...

>GENOME_Gekko_japonicus.uce-4621 Gekko japonicus genome ultra conserved element uce-4621
TTAGTGATATAGTTGATCATTGAATTCTGTCTTCTATATTAAATTAGAAGAATGTTTAAA...
```

In this way, it is very important that the input fasta files are labeled following the scheme `Genus_species.fasta`, 
as illustrated in the example in Step 6. Notice also that the bases are automatically converted into uppercase.



## Instructions for Usage

To run the script, you can use it in the following way:

```
python phyluce-genomes-to-supercrunch.py -i <input directory> -o <output directory>
```

#### Argument Explanations:

##### `-i <path-to-directory>`

> The full path to a directory that contains all the input fasta files. These are the fasta files generated by Phyluce, which contain UCE sequences extracted from genomes.

##### `-o <path-to-directory>`

> The full path to an existing directory to write the output files.


#### Example Use:

```
python phyluce-genomes-to-supercrunch.py -i bin/Analysis/Input-fasta-files -o bin/Analysis/Output/
```


## Example Data

There are UCE sequences extracted from 21 genomes using Phyluce available in the [example-data folder](https://github.com/dportik/phyluce-genomes-to-supercrunch/tree/master/example-data),
called `21-genome-extractions.zip`. The output of running this script for these 21 fasta files is also provided
in this folder, and is called `Genome_UCE_Seqs.fasta.zip`. You can test running this script on this example
data set before using it for your own data.


## Contact

`phyluce-genomes-to-supercrunch.py` was written by Daniel Portik (daniel.portik@gmail.com)
