/*
 * microcode_ctl - Manipulate /dev/cpu/microcode under Linux
 *
 * Copyright 2000 (c) Simon Trimmer, Tigran Aivazian.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version
 * 2 of the License, or (at your option) any later version.
 *
 */

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>

static char *progname;
int print_normal_messages=1;
int print_error_messages=1;

#define BUFFER_SIZE	4096
#define MAX_MICROCODE	2000000

#define MICROCODE_DEVICE_DEFAULT	"/dev/cpu/microcode"
#define MICROCODE_FILE_DEFAULT		"/etc/microcode.dat"

static void usage(void)
{
	fprintf(stderr, "\nThis program is for updating the microcode on Intel processors\n"
			"belonging to the IA32 family - PentiumPro upwards (x86_64 included).\n"
			"It depends on the Linux kernel microcode driver.\n\n"
			"Usage: %s [-h] [-u] [-q] [-Q] [-f microcode]\n\n"
			"  -h	this usage message\n"
			"  -q	run silently when successful\n"
			"  -Q	run silently even on failure\n"
			"  -u	upload microcode (default filename:\"%s\"\n"
			"  -f	upload microcode from named Intel formatted file\n\n", 
			progname, MICROCODE_FILE_DEFAULT);
	exit(1);
}

/* 
 * The update has two stages; 
 * a) read in the Intel microcode file and convert it into a format suitable
 *    for the processor.
 * b) send the microcode to the driver which applies the update
 */
static int do_update(char *device, char *filename)
{
	FILE *fp;
	char line_buffer[BUFFER_SIZE];
	int microcode[MAX_MICROCODE];
	int *pos;
	int outfd;
	int wrote, length;


	if( (fp=fopen(filename, "r")) == NULL){
		if(print_error_messages)
			fprintf(stderr, "%s: cannot open source file '%s' errno=%d (%s)\n",
				progname, filename, errno, strerror(errno));
		return errno;
	}

	pos = microcode;

	while(fgets(line_buffer, BUFFER_SIZE, fp) != NULL) {
		 /*
		  * Data lines will are of the form "%x, %x, %x, %x", therefore
		  * lines start with a 0
		  */
                if(*line_buffer == '0'){
			sscanf(line_buffer, "%x, %x, %x, %x", pos,
					(pos + 1), (pos + 2), (pos + 3));
			pos += 4;
		}

		if (MAX_MICROCODE < (pos - microcode)){
			/* not checking the buffer length could cause grief? */
			if(print_error_messages)
				fprintf(stderr, "%s: file too large for utility microcode buffer\n"
						"%s: change MAX_MICROCODE yourself :)\n", progname, progname);
			fclose(fp);	
			return errno;
		}
		
	}

	fclose(fp);
	length = sizeof(int) * (pos - microcode);
	if(print_normal_messages)
		fprintf(stderr, "%s: writing microcode (length: %d)\n",  progname, length);
	
	if((outfd = open(device, O_WRONLY)) == -1){
		if(print_error_messages)
			fprintf(stderr, "%s: cannot open %s for writing errno=%d (%s)\n",
				progname, device, errno, strerror(errno));
		return errno;
	}

	if( (wrote = write(outfd, &microcode, length)) < 0){
		if(print_error_messages)
			fprintf(stderr, "%s: error writing to '%s' errno=%d (%s)\n"
					"%s: there may be messages from the driver in your system log.\n",
				progname, device, errno, strerror(errno), progname);
		close(outfd);
		return errno;
	}

	if((wrote == length) && print_normal_messages)
			fprintf(stderr, "%s: microcode successfuly written to %s\n",
			       progname, device);

	close(outfd);

	return errno;
}

int main(int argc, char *argv[])
{
	int c;
	static char device[2048];
	static char filename[2048];
	int upload=0;
	int return_code;

	progname = argv[0];

	strcpy(device, MICROCODE_DEVICE_DEFAULT);
	strcpy(filename, MICROCODE_FILE_DEFAULT);
	
	while (EOF != (c = getopt(argc, argv, "hqQiud:f:"))) {
		switch(c) {
			case 'h':
				usage();

			case 'q':
				print_normal_messages=0;
				break;

			case 'Q':
				print_error_messages=0;
				print_normal_messages=0;
				break;

			case 'd':
				strcpy(device, optarg);
				break;

			case 'u': /* do a microcode upload */
				upload++;
				break;

			case 'f': /* set microcode file to optarg and upload */
				upload++;
				strcpy(filename, optarg);
				break;

			case '?':
				usage();
		}
	}

	if (upload) {
		if((return_code = do_update(device, filename)))
			exit(return_code);
	} else
		usage();

	return 0;
}
