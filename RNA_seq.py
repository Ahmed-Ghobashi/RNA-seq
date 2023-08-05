#!/usr/bin/env python

### Authors: Ahmed Ghobashi
### 2023

###

import subprocess
import os
import argparse

def cmdLine():

    parser=argparse.ArgumentParser()
    parser.add_argument('-n','--name',dest='name',type=str,default='RNA-seq_run',help='substring to have in our output files')
    parser.add_argument('-j','--job',dest='job',type=str,default='ALL', choices=['ALL','Fastqc','Genomic_index','Count'])
    parser.add_argument('-sd', '--save_dir', dest='save_dir', type=str, default='results')
    parser.add_argument('-th', '--thread_core', dest='thread_core', type=str, default='2')
    parser.add_argument('-i', '--genome_index', dest='genome_index', type=str, default='TRUE', choices=['TRUE','FALSE'])
    parser.add_argument('-gd', '--genome_dir', dest='genome_dir', type=str)#directory for the genome index
    parser.add_argument('-fa', '--fasta_dir', dest='fasta_dir', type=str)##directory of fasta file
    parser.add_argument('-gtf', '--gtf_dir', dest='gtf_dir', type=str)##directory of GTF file
    parser.add_argument('-c', '--condition', dest='condition', type=str)###write the sample name and replicate
    parser.add_argument('-r1', '--read1', dest='read1', type=str)##read of your sample
    parser.add_argument('-p', '--paired', dest='paired', type=str,default='NO',choices=['YES','NO'])
    parser.add_argument('-r2', '--read2', dest='read2', type=str)
    parser.add_argument('-s', '--strandness', dest='strandness', type=str,default='1',choices=['0','1','2'],
                help='0 for unstranded reads, 1 for stranded reads and 2 for reversely stranded reads. This depends on the library used in the sequencing protocol. Deafault '
                     'is 1 as most commercial kits use standed protocol')


    args=parser.parse_args()

    ##creating directory to save the results
    cwd=os.getcwd()
    path=os.path.join(cwd,args.save_dir)

    if not os.path.isdir(path): os.mkdir(path)

    ##build a command for fastqc

    #os.mkdir(os.path.join(args.save_dir,'fastqc'))

    if args.job=='Fastqc' or args.job=='ALL':
        fastq_path=os.path.join(path,'fastqc')

        if not os.path.isdir(fastq_path): os.mkdir(fastq_path)
    #path=os.path.realpath(os.path.join(args.save_dir,'fastqc'))

        if args.paired== 'NO':
            cmd=['fastqc', args.read1, '-o' , fastq_path]
            cmd=' '.join(cmd)
        else:
            cmd = ['fastqc', args.read1, args.read2,'-o', fastq_path]
            cmd = ' '.join(cmd)

    ##run the command
        print('*******Runing FASTQC*********')

        subprocess.run(cmd, shell=True,check=True)

    ##creating genome index for alignemnt

    elif args.job == 'Genomic_index' or args.job=='ALL':
        if args.genome_index =='FALSE':
            index_cmd=['STAR', '--runThreadN', args.thread_core
               ,'--runMode genomeGenerate', '--genomeDir',args.genome_dir, '--genomeFastaFiles', args.fasta_dir, '--sjdbGTFfile',args.gtf_dir]

            index_cmd=' '.join(index_cmd)

    ##generating the index
            print('*******GENERATING GENOME INDEX BASED ON THE PROVIDED GTF AND FASTA FILES*********')

            subprocess.run(index_cmd,shell=True,check=True)

    ##aligning using STAR

    #os.mkdir(os.path.join(args.save_dir, 'RNA_aligment'))
        RNA_aligment=os.path.join(path,'RNA_aligment')

        if not os.path.isdir(RNA_aligment): os.mkdir(RNA_aligment)

    #path = os.path.realpath(os.path.join(args.save_dir, 'RNA_aligment'))
        path_ = os.path.realpath(RNA_aligment)
        path_result = [path_, '/', args.condition]
        path_result = ''.join(path_result)


        align_cmd=['STAR','--runThreadN', args.thread_core,'--genomeDir',args.genome_dir,'--runMode alignReads','--outSAMtype BAM SortedByCoordinate',
               '--quantMode GeneCounts','--outFileNamePrefix', path_result, '--readFilesIn', args.read1]

        if args.paired=='YES':
            align_cmd.append(args.read2)


        if args.read1[-2:]=='gz':
            align_cmd.append('--readFilesCommand zcat')


        align_cmd=' '.join(align_cmd)

    ##aligning the genome
        print('*******DOING THE ALIGNING *********')
        subprocess.run(align_cmd, shell=True, check=True)



    ###generating the count matrix
    elif args.job=='Count' or args.job=='ALL':

        count = os.path.join(path, 'Counts')

        if not os.path.isdir(count): os.mkdir(count)##make directory for count matrix
    #os.mkdir(os.path.join(args.save_dir, 'Counts'))##make directory for the counts


        count_output = [count, '/', args.condition,'.txt']##
        count_output=''.join(count_output)

        RNA_aligment = os.path.join(path, 'RNA_aligment')

        if not os.path.isdir(RNA_aligment): os.mkdir(RNA_aligment)

        path_RNA = os.path.realpath(RNA_aligment)##read the bam file in RNA aligment
        bam=[path_RNA,'/',args.condition,'Aligned.sortedByCoord.out.bam']
        bam = ''.join(bam)

        count_cmd=['featureCounts', '-F GTF --primary -t exon -g gene_id --minOverlap 10','-T', args.thread_core,'-s', args.strandness,'-a',args.gtf_dir, '-o', count_output, bam]

        if args.paired=='YES':
            count_cmd.append('-p -B -C')

        count_cmd=' '.join(count_cmd)

    ##aligning the genome
        print('*******RUNNING FEATURECOUNT *********')
        subprocess.run(count_cmd,shell=True, check=True)

if __name__== "__main__":
    cmdLine()



