#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {

	int i, j, pid, status;

	char *set;
	char *core;

	i = 3; j = 4;
	for(i = 3; i <= 24; i *= 2) {
		for(j = 4; j <= 256; j *= 4) {
	
			switch(pid = fork()) {
				case 0:
					sprintf(set,"%u",i);
					sprintf(core,"%u",j);
					char *args[];
					args = {"python","runExp.py",set,"0"};
					//printf("%s\n",set);
					//printf("%s\n",core);
					execvp("python","python","python",);
					printf("i = %u, j = %u\n",i,j);
					exit(0);
	
				default:
					waitpid(pid,&status,0);		
					break;
			}
		}
	}	


	return 0;
}
