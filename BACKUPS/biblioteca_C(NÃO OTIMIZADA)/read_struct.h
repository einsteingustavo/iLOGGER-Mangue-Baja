#ifndef STRUCT_READ_H
#define STRUCT_READ_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define NUM_PACKETS 50

typedef struct
{
    int16_t acclsmx;
    int16_t acclsmy;
    int16_t acclsmz;
    int16_t anglsmx;
    int16_t anglsmy;
    int16_t anglsmz;
    uint16_t A0;
    uint16_t A1;
    uint16_t A2;
    uint16_t pulses_chan1;
    uint16_t pulses_chan2;
    uint32_t timestamp;
} packet;


void read_struct(char foldername[80], int RUN);

#endif
