#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys, os
import argparse
from datetime import datetime

now = datetime.now() # current date and time



def add_args(a):
    """
    Parses arguments for program.
    """
    parser = argparse.ArgumentParser(description=""" Test description """)
    parser.add_argument(
        "--accessionsfile",
        "-a",
        help="Provide path and filename of accessions file",
        required=True,
    )
    parser.add_argument(
        "--assemblycol",
        "-c",
        help="Accession column name in accessions file",
        required=True,
    )
    parser.add_argument(
        "--NCBI",
        "-n",
        help="Provide pre-downloaded NCBI assembly summary from https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt",
    )
    args = parser.parse_args(a)
    return args


def get_assembly_summary():
    d = now.strftime("%b-%d-%Y")
    cmd = f'wget https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt'
    os.system(cmd)
    return(f'assembly_summary_genbank.txt')

def find_matching_accessions(sfilename, assemblycol, afilename):
     NCBI_df = pd.read_csv(sfilename, delimiter='\t', skiprows=1)
     acc_df = pd.read_csv(afilename)

     accessionlist=list(acc_df[assemblycol])
     NCBI_matched = NCBI_df[NCBI_df['biosample'].isin(accessionlist)]

     for x in NCBI_matched['ftp_path']:
         dcmd = f'wget {x} .'
    print(dcmd)


if __name__ == "__main__":
    args = add_args(sys.argv[1:])

    sfilename = ''
    if args.NCBI:
        sfilename=args.NCBI
    else:
        sfilename = get_assembly_summary()

    find_matching_accessions(sfilename, args.assemblycol, args.accessionsfile)
