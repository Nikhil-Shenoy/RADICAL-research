#include <stdio.h>

int main(int argc, char *argv[]) {


	char *in = argv[1];
	char *out = argv[2];

	FILE *input = fopen(in,"r");
	FILE *output = fopen(out,"w");

	char c;
	int counter;
	counter = 0;
	char buffer[50];
	while((c = fgetc(input)) != EOF) {
		buffer[counter] = c;
		counter++;	
	}

	while(counter > -1) {
		fputc(buffer[counter],output);
		counter--;
	}

	printf("Finished with the reversal\n");

	fclose(input);
	fclose(output);

	return 0;
}
