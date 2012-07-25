/*
 * microcode_ctl - Manipulate /dev/cpu/microcode under Linux
 *
 * Copyright 2000 (c) Tigran Aivazian, Simon Trimmer.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version
 * 2 of the License, or (at your option) any later version.
 *
 *	1.0	09 June 2000,	Simon Trimmer <simon@veritas.com>
 *				Tigran Aivazian <tigran@sco.com>
 * 		Initial release
 *	1.01	19 June 2000,	Simon Trimmer <simon@veritas.com>
 * 		general tidy up and argument sequencing fix
 * 		added default microcode filename and -u switch
 * 				
 */
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>

#include <asm/processor.h>

static char *progname;

#define BUFFER_SIZE	4096
#define MAX_MICROCODE	2000000

#define MICROCODE_DEVICE_DEFAULT	"/dev/cpu/microcode"
#define MICROCODE_FILE_DEFAULT		"/etc/microcode.dat"

static void usage(void)
{
	fprintf(stderr, "\nThis program is for updating the microcode on Intel processors\n"
			"belonging to the P6 family - PentiumPro, Pentium II, Pentium III etc.\n"
			"It depends on the Linux kernel microcode driver.\n\n"
			"Usage: %s [-h] [-i] [-u] [-f microcode]\n\n"
			"  -h 		this usage message\n"
			"  -i 		release any buffers held in microcode driver\n"
			"  -u		upload microcode (default filename:\"%s\"\n"
			"  -f		upload microcode from named Intel formatted file\n\n", progname, MICROCODE_FILE_DEFAULT);
}

static int do_ioctl(char *device, int cmd)
{
	int fd;
	int error = 0;

	fd = open(device, O_RDONLY);
	if (fd == -1) {
		fprintf(stderr, "%s: open(%s), errno=%d (%s)\n",
				progname, device, errno, strerror(errno));
		return 1;
	}
	if (ioctl(fd, cmd, 0) == -1) {
		fprintf(stderr, "%s: ioctl(cmd=%d), errno=%d (%s)\n",
				progname, cmd, errno, strerror(errno));
		error = 2;
	}
	(void)close(fd);
	if(!error)
		fprintf(stderr, "%s: microcode buffers released\n", progname);

	return error;
}

/* 
 * The update has two stages; 
 * a) read in the Intel microcode file and convert it into a format suitable
 *    for the processor.
 * b) send the microcode to the driver which apples the update
 */
static int do_update(char *device, char *filename)
{
	FILE *fd;
	char line_buffer[BUFFER_SIZE];
	int microcode[MAX_MICROCODE];
	int *pos;
	int outfd;
	int wrote, length;


	if( (fd=fopen(filename, "r")) == NULL){
		fprintf(stderr, "%s: cannot open source file '%s' errno=%d (%s)\n",
				progname, filename, errno, strerror(errno));
		return 1;
	}

	pos = microcode;

	while(fgets(line_buffer, BUFFER_SIZE, fd) != NULL) {
		if(*line_buffer != '/'){
			sscanf(line_buffer, "%x, %x, %x, %x", pos,
					(pos + 1), (pos + 2), (pos + 3));
			pos += 4;
		}

		if (MAX_MICROCODE < (pos - microcode)){
			/* not checking the buffer length could cause grief? */
			fprintf(stderr, "%s: file too large for utility microcode buffer\n"
					"%s: change MAX_MICROCODE yourself :)\n", progname, progname);
			fclose(fd);	
			return 1;
		}
		
	}

	fclose(fd);
	length = sizeof(int) * (pos - microcode);
	fprintf(stderr, "%s: writing microcode (length: %d)\n",  progname, length);
	
	if((outfd = open(device, O_WRONLY)) == -1){
		fprintf(stderr, "%s: cannot open %s for writing errno=%d (%s)\n",
				progname, device, errno, strerror(errno));
		return 1;
	}

	if( (wrote = write(outfd, &microcode, length)) < 0){
		fprintf(stderr, "%s: error writing to '%s' errno=%d (%s)\n"
				"%s: there may be messages from the driver in your system log.\n",
				progname, device, errno, strerror(errno), progname);
		close(outfd);
		return 1;
	}

	if(wrote == length)
		fprintf(stderr, "%s: microcode successfuly written to %s\n",
			       progname, device);

	close(outfd);

	return 0;
}

int main(int argc, char *argv[])
{
	int c;
	static char device[2048];
	static char filename[2048];
	int upload=0, freeflag=0;
	int return_code;

	progname = argv[0];

	if (argc == 1) {
		usage();
		exit(1);
	}
	
	strcpy(device, MICROCODE_DEVICE_DEFAULT);
	strcpy(filename, MICROCODE_FILE_DEFAULT);
	
	while (EOF != (c = getopt(argc, argv, "hiud:f:"))) {
		switch(c) {
			case 'h':
				usage();
				exit(1);

			case 'd':
				strcpy(device, optarg);
				break;

			case 'i': /* send the ioctl to free the buffers */
				freeflag++;
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
				exit(1);
		}
	}

	if (upload)
		if((return_code = do_update(device, filename)))
			exit(return_code);
		
	if (freeflag)
		exit(do_ioctl(device, MICROCODE_IOCFREE));
			
	usage();
	return 0;
}
