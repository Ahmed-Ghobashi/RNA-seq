# RNA-seq Automation
This work performs a Fastqc, generates a Genome index, genome aligning using STAR, and count matrix using subread

Start by cloning the source code:
```
git clone https://github.com/Ahmed-Ghobashi/RNA-seq.git
cd RNA-seq
```

if you are working on HPC, you could load the dependencies using the ```module load``` function

or
You can create the virtual sofware environment, and download all software and dependencies.
Create the new environment and specify the software to include in it.
```
conda create -n < name of your environment > -y -c conda-forge -c bioconda \
pandas fastqc star samtools subread
```
    
Now you can activate your environment ```conda activate <name of your environment>```.

## RNA-seq automation
In the terminal 
```
pyhton RNA_seq.py 
-n, --name---> name of your job,default='RNA-seq_run'
-j, --job'-->default='ALL', choices=['ALL','Fastqc','Genomic_index','Count']
-sd, --save_dir--->default='results', name of the result directory
-th, --thread_core-->default='2', number of the cores
-i, --genome_index--> ask if you have genome index, default='TRUE', choices=['TRUE','FALSE'])
-gd', --genome_dir--> directory for the genome index
-fa, --fasta_dir-->directory of fasta file
-gtf, --gtf_dir-->directory of GTF file
-c, --condition-->write the sample name and replicate
-r1, --read1-->read number 1 of your sample
-p, --paired--> the sequencing is paired or single end ,default='NO',choices=['YES','NO']
-r2, --read2-->read number 2 of your sample (for paired-end only)
-s, --strandness--> 0 for unstranded reads, 1 for stranded reads and 2 for reversely stranded reads. This depends on the library used in the sequencing protocol. 
                     <Most commercial kits use standed protocol',default='1',choices=['0','1','2']
```

For example
```
 python RNA_seq.py -th 6 -gd /N/slate/aghobash/STAR/Genecod -fa /N/slate/aghobash/STAR/GRCh38.primary_assembly.genome.fa\
 -gtf /N/slate/aghobash/STAR/gencode.v29.annotation.gtf -c EV_1 -r1 GSF3258-mRNAseq-9_S19_R1_001.fastq.gz\
 -p YES -r2 GSF3258-mRNAseq-9_S19_R2_001.fastq.gz
```

## This work depends on

**FastQC** - Read quality control.\
**STAR** - Read aligner.\
**Samtools** - SAM/BAM manipulation.\
**Subread** - Read annotation and counting.




                    
