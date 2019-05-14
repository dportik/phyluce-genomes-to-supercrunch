# phyluce-genomes-to-supercrunch

---------------

## Overview

`phyluce-genomes-to-supercrunch.py` is a python script that can be used to
combining the genome-extracted UCE sequences in multiple fasta files output by Phyluce, 
and converting them into a fasta record labeling format that is similar to GenBank records.
This format is compatible with [SuperCRUNCH](https://github.com/dportik/SuperCRUNCH) and 
allows all UCE data to be parsed correctly using an appropriate locus search terms file 
(such as tetrapod-5k). To work properly, the input fasta files (which come from Phyluce) 
should be labeled with the following format: `Genus_species.fasta`.

## Installation

`phyluce-genomes-to-supercrunch.py` is written in Python (2.7) and functions as a stand-alone 
command-line script. It can be downloaded and executed independently without the need to 
install any additional Python packages or libraries, making it easy to use and edit.

## License

GNU Lesser General Public License v3.0

## Explanation and Instructions for Usage

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

4. Run `phyluce_probe_run_multiple_lastzs_sqlite` from Phyluce to generate an SQL database, using the `uce-5k-probes.fasta` file.

5. Run `phyluce_probe_slice_sequence_from_genomes` from Phyluce to extract UCE sequences into fasta files.

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
fasta file that is compatible with SuperCRUNCH. The general format of the new description lines is:

```
>GENOME_[taxon].[uce-label] [taxon] ultra conserved element [uce-label]
```

Here, the `taxon` label will be the name of the output fasta file, and the `uce-label` will be pulled
from the description lines. So, let's say the input fasta file that contained the record labels above
is called `Gekko_japonicus.fasta`. The records above will be converted into the following:

```
>GENOME_Gekko_japonicus.uce-502 Gekko japonicus ultra conserved element uce-502
CATTATTAGAGAGCTCTTTCTAGTAAGCCTTTAAAAAAAAAAAAAAAGAAAAAAAAGAAA...

>GENOME_Gekko_japonicus.uce-507 Gekko japonicus ultra conserved element uce-507
TGTAATGTATTTCATGTTTAGCACCTATTTATTCCATGTAACTTCACCATATCAAATGAG...

>GENOME_Gekko_japonicus.uce-5821 Gekko japonicus ultra conserved element uce-5821
CAGTTGCAAGACAAACATGTATGGGAGGCAGAATGGGGAGGGAAATTAAACACATCAAGA...

>GENOME_Gekko_japonicus.uce-4621 Gekko japonicus ultra conserved element uce-4621
TTAGTGATATAGTTGATCATTGAATTCTGTCTTCTATATTAAATTAGAAGAATGTTTAAA...
```

In this way, it is very important that the input fasta files are labeled following the scheme `Genus_species.fasta`, 
as illustrated in the example in Step 6. Notice also that the bases are automatically converted into uppercase.



