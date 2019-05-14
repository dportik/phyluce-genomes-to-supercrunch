import os
import argparse
from datetime import datetime

def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
            description="""---------------------------------------------------------------------------
    phyluce-genomes-to-supercrunch: A script for combining the genome-extracted
    UCE sequences in multiple fasta files output by Phyluce, and converting
    them into a fasta record labeling format that is similar to GenBank records.
    This format is compatible with SuperCRUNCH and allows all UCE data to be 
    parsed correctly using an appropriate locus search terms file (such as tetrapod-5k).
    Full instructions for script usage are available at: 
    https://github.com/dportik/phyluce-genomes-to-supercrunch.
	---------------------------------------------------------------------------""")
    parser.add_argument("-i", "--in_dir", required=True, help="REQUIRED: The full path to a directory which contains the genome-extracted fasta files from Phyluce.")
    parser.add_argument("-o", "--out_dir", required=True, help="REQUIRED: The full path to an existing directory to write output files.")
    return parser.parse_args()

def fasta_dict(f):
    '''
    Function to convert a fasta file into
    dictionary structure with custom key name
    and sequence as value.
    
    For example, the following fasta description line from genome file 'Alligator_mississippiensis.fasta':
    
    >Node_0_length_1119_cov_1000|contig:AKHW03001146.1|slice:26076133-26077252|uce:uce-502|match:26076632-26076752|orient:set(['+'])|probes:1
    
    is converted into:
    
    >GENOME_Alligator_mississippiensis.uce-502 Alligator mississippiensis ultra conserved element uce-502
    '''
    
    print "\tProcessing {}...".format(f)
    #get the name of the taxon, which is assumed to be
    #the fasta file name, e.g. 'Alligator_mississippiensis.fasta'
    taxon = f.split('.')[0]
    #initiate empty dictionary to store fasta contents
    f_dict = {}
    #put cleaned lines from fasta file into list
    with open(f, 'r') as fh:
        lines = [l.strip() for l in fh if l.strip()]
    #iterate over lines and create fasta dictionary
    for line in lines:
        if line.startswith(">"):
            #find uce label in records formatted as such:
            #>Node_1_length_1120_cov_1000|contig:AKHW03000416.1|slice:16386850-16387970|uce:uce-507|match:16387350-16387470|orient:set(['+'])|probes:1
            #>Node_2_length_1120_cov_1000|contig:AKHW03006853.1|slice:14925567-14926687|uce:uce-211|match:14926067-14926187|orient:set(['+'])|probes:1
            #use list comprehension plus additional string split
            uce = [l for l in line.split("|")][3].split(':')[1]
            #create new description line that fits the general structure:
            #>GENOME_[taxon].[uce-label] [taxon] ultra conserved element [uce-label]
            new_key = ">GENOME_{0}.{1} {2} ultra conserved element {1}".format(taxon, uce, taxon.replace("_", " "))
            f_dict[new_key] = ""
        else:
            f_dict[new_key] += line.upper()
    return f_dict

def write_fasta(d):
	'''
	Simple function to iterate over each fasta dictionary
	and write the key, val pairs to the same output file.
	'''
    outname = "Genome_UCE_Seqs.fasta"
    with open(outname, 'a') as fh:
        for key, val in d.iteritems():
            fh.write("{}\n{}\n".format(key, val))

def run_tasks(in_dir, out_dir):
	'''
	Function to navigate to correct directories to
	either find fasta files and convert to dictionary
	structures or write the final output file.
	'''
    os.chdir(in_dir)
    f_list = sorted([f for f in os.listdir('.') if f.endswith(".fasta") or f.endswith(".fa")])
    print "Found {} fasta files to process.".format(len(f_list))
    #list comprehension to generate a list of dictionaries using function fasta_dict()
    #each of which contains the contents of a particular fasta file
    dict_list = [fasta_dict(f) for f in f_list]
    os.chdir(out_dir)
    print "Writing data to Genome_UCE_Seqs.fasta."
    for d in dict_list:
        write_fasta(d)
            
def main():
    args = get_args()
    tb = datetime.now()
    run_tasks(args.in_dir, args.out_dir)
    tf = datetime.now()
    te = tf - tb
    print "\nFinished.\nElapsed time: {} (H:M:S)\n".format(te)

if __name__ == '__main__':
    main()

