#BSUB -q qhpc2
#BSUB -app fluent
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -n 10
#BSUB -R "span[hosts=1]"  
fluent 3ddp -g -pib -mpi=intel -i inputfile.jou -t8
