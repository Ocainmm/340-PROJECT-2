#include<stdio.h>
#include <stdlib.h>

typedef struct job
{
int id;
int mem;
int rt;
int start;
int end;
}job;
//rand() only allows the use of a upper value so a function to make a rand with a upper and lower bound
int random(int lower, int upper)
{
	return (rand() % (upper - lower + 1)) + lower;
}
int main(int argc, char *argv[])
//int main(int totalMem, int pageMem, int jobNum, int minRt, int maxRt, int minMem, int maxMem)
{
	//check args
	if (argc < 7) {
		printf("ERROR: Improper use. 7 integer inputs required.");
		exit(0);
	}
	//check users math
	if((totalMem % pageMem) != 0){
		printf("ERROR: Improper use. Memory size, argument 1, should be an even multiple of page size, argument 2.");
		exit(0);
	}
	//rename arguments for readability
	int totalMem = atoi(argv[0]);
	int pageMem = atoi(argv[1]);
	int jobNum = atoi(argv[2]);
	int minRt = atoi(argv[3]);
	int maxRt = atoi(argv[4]);
	int minMem = atoi(argv[5]);
	int maxMem = atoi(argv[6]);
	//initialize page table as array 0=free
	int pageNum = totalMem/pageMem;
	int page[pageNum];
	int i = 0;
	for(i; i<pageNum; i++){
		page[i]=0;
	}
	//initialize job array all jobs will start in round 1 but end is 0 as a placeholder
	struct job jobs[jobNum];
	for (i = 0; i < jobNum; i++){
		jobs[i].id = i+1;
		jobs[i].mem = random(minMem, maxMem);
		jobs[i].rt = random(minRt, maxRt);
		jobs[i].start = 1;
		jobs[i].end = 0;
		printf("job %d memory size: %d runtime: %d", jobs[i].id, jobs[i].mem, jobs[i].rt);
		//printf("job %d memory size: %d runtime: %d", jobs[0].id, jobs[0].mem, jobs[0].rt);
	}
}
