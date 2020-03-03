#include<stdio.h>
#include <stdlib.h>

struct job
{
int id;
int mem;
int rt;
int start;
int end;
}
//rand() only allows the use of a upper value so a function to make a rand with a upper and lower bound
int random(int lower, int upper)
{
	int num = (rand() % (upper - lower + 1)) + lower; 
	return num;
}
int main(int totalMem, int pageMem, int jobs,int minRt, int maxRt, int minMem, int maxMem)
{
	//check users math
	if((totalMem % pageMem) != 0){
		printf("ERROR: Improper use. Memory size should be an even multiple of page size.");
	exit(0);
	}
	int pageNum = totalMem/pageMem;
	//initialize page table as array 0=free
	int page[pageNum];
	for(int i=0; i<pageNum; i++){
		page[i]=0;
	}
}