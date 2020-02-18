import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import subprocess as sp
import shlex
import os
import argparse

def pca_first_round(fp = 'data/interim/chr22', fn = "chr22_test.vcf.gz"):
    if not os.path.exists("data/interim"):
        cmd = shlex.split('mkdir -p data/interim')
        sp.call(cmd, shell = True)
    sp.call('plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/chr22_test.vcf.gz   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/chr22', shell = True)
    sp.call('plink2 --bfile data/interim/chr22 --pca', shell = True)

def remove_outlier(file = 'plink.eigenvec'):
    # read the vcf file as a dataframe
    tb = pd.read_table(file, header = None, sep = ' ')

    # calculate the standard deviation and multiply it by 2
    twostdv = np.std(tb[2])*2

    #reindex
    temp = tb.set_index(tb[0])
    temp = temp.drop([0,1], axis = 1)

    # choose the first 10 components
    temp = temp.iloc[:, 0:10]
    #select the outliers, which are two standard deviation away from the mean
    ol = (temp.abs()<twostdv).all(axis = 1)
    ollist = list(ol[ol == False].index)
    #write the outlier list into a text file
    with open('ollist.txt', 'w') as filehandle:
        for listitem in o:
            filehandle.write('%s\n' % listitem)

def first_plot(file = 'plink.eigenvec'):
    tb = pd.read_table(file, header = None, sep = ' ')
    tb.plot(2,3, kind = 'scatter')

def pca_second_round(fp = 'data/interim/chr22'):
    sp.call('plink2 --bfile ' + fp + ' --remove-fam listfile.txt --pca', shell = True)

def second_plot(file = 'plink.eigenvec'):
    tb = pd.read_table(file, header = None, sep = ' ')
    tb.plot(2,3, kind = 'scatter')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('data', help='an integer for the accumulator')
parser.add_argument('process', help='sum the integers (default: find the max)')

args = parser.parse_args()


if args.process == 'pca':
    print(2)
    pca_first_round()
elif args.process == 'outlier':
    remove_outlier()
elif args.process == 'first_plot':
    first_plot()
elif args.process == 'pca_second':
    pca_second_round()
elif args.process == 'second_plot':
    second_plot()
else:
    print(1)
    #pca_first_round('data/interim/chr22', "chr22_test.vcf.gz")




#mkdir -p data/interim
#plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/chr22_test.vcf.gz   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/chr22
#plink2 --bfile data/interim/chr22 --pca
#plink2 --bfile data/interim/chr22 --remove-fam listfile.txt --pca

