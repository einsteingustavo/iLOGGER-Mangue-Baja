#include "read_struct.h"

void read_struct(char foldername[80], int RUN)
{
    char error, first = 0;
    int  part = 0;
    char filename[80];
    FILE *f, *fp;

    error = 0;
    part = 0;

    if(RUN < 0)
        return;

    sprintf(filename, "%s/RUN%d.csv", foldername, RUN);
    f = fopen(filename, "wt");
    // printf("file = %ld\r\n", f);

    fprintf(f, "lsmaccx,lsmaccy,lsmaccz,lsmangx,lsmangy,lsmangz,a0,a1,a2,f1,f2,timestamp\n");

    char name[70];
    sprintf(name, "%s/%s%d/%s%d", foldername,"RUN", RUN, "part", part+1);
    printf("filename = %s\n", name);
    fp = fopen(name, "rb");
    packet x[NUM_PACKETS];

    if (fp == NULL)
    {
        error = 1;
        return;
    }

    printf("\n~~~~~~~~PART %d ~~~~~~~~", part);

    while(1)
    {
        fread((void *)x, sizeof(packet), 1, fp);
        fprintf(f, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n", x->acclsmx, x->acclsmy, x->acclsmz, x->anglsmx, x->anglsmy, x->anglsmz, x->A0, x->A1, x->A2,
        x->pulses_chan1, x->pulses_chan2, x->timestamp);
        if (feof(fp)) break;
    }
    fclose(fp);
    fp = NULL;
    fclose(f);
    f = NULL;

}

