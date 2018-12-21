#!/usr/bin/env python2

"""
Script to plot the distribution of lengths of a fasta file.

Written by Wenchao Lin.

You can use this script from the shell like this:
$ ./fasta_length_hist.py --input sample.fasta --output seqs.pdf --min 200 --max 400
"""

###############################################################################
# Modules #
import argparse, sys, time, getpass, locale
from argparse import RawTextHelpFormatter
from Bio import SeqIO
import numpy as np

# Matplotlib #
import matplotlib
matplotlib.use('Agg', warn=False)
from matplotlib import pyplot as plt

################################################################################
desc = "fasta_length_hist.py v1.0"
parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter, add_help=True)

# All the required arguments #
parser.add_argument('-i','--input', help="The fasta file to process", type=str,required=True)


# All the optional arguments #
parser.add_argument('-o','--output', default="seqHist", help='The output file of the histogram. Default:seqHist.pdf', type=str)
parser.add_argument('-of','--format', default='pdf', help='Set ouput format. Default to "pdf"', type=str,choices=('pdf','png','jpeg'))

parser.add_argument("--x_log", action='store_true' ,help='xAxis will be set to a log scale')
parser.add_argument("--y_log", action='store_true' ,help='yAxis will be set to a log scale')
parser.add_argument("--grid", action='store_true', help='Trun on grid of the plot')

parser.add_argument("--xmin", help="Set the limits (min) of x-axis")
parser.add_argument("--xmax", help="Set the limits (max) of x-axis ")


# Parse it #
args        = parser.parse_args()

if args.input: 
	input_path  = args.input
else:
	parser.print_help()
	exit(0)

output_path = args.output + '.' + args.format

x_log       = bool(args.x_log)
y_log       = bool(args.y_log)
show_grid   = bool(args.grid)


################################################################################
# Read #
lengths = map(len, SeqIO.parse(input_path, 'fasta'))

# Report #
sys.stderr.write("Making graph...\n")

# Data #
values = [float(i) for i in lengths]


# Plot #
fig   = plt.figure()
axes  = plt.hist(values,color='red', bins=500)
fig   = plt.gcf()
title = 'Distribution of sequence lengths'
# axes.set_title(title)
plt.xlabel('Seqence length',fontsize=11,fontweight='bold')
plt.ylabel('Number of sequences',fontsize=11,fontweight='bold')
plt.grid(show_grid)


# Log #
if x_log: plt.yscale('symlog')
if y_log: plt.xscale('symlog')
if args.xmin: plt.xlim(left=float(args.xmin))
if args.xmax: plt.xlim(right=float(args.xmax))


# Adjust #
width=8.0; height=4.0; bottom=0.14; top=0.95; left=0.1; right=0.95
fig.set_figwidth(width)
fig.set_figheight(height)
fig.subplots_adjust(hspace=0.0, bottom=bottom, top=top, left=left, right=right)


# Save it #
sys.stderr.write("Saved graph to %s\n" % output_path)
fig.savefig(output_path, format=args.format)
