# Overview

We will define a set of chromosomes that will provide definitions that will
allow us to generate music.

## Chromosome

A chromosome will be defined as the combination of a set of genes and a
chromosome designator. The *genes* will simply be `1` or `0` bits, and the
designator will tell us what kind of chromosome it is so that we know how to
parse its data.

## Notes

When we refer to notes in a chromosome, we will use the following mapping. The
sequences `1100` through `1111` are undefined.

| Decimal Number | Gene Sequence | Note |
-----------------------------------------
| 0              | 0000          | C    |
| 1              | 0001          | C♯/D♭ |
| 2              | 0010          | D    |
| 3              | 0011          | D♯/E♭ |
| 4              | 0100          | E    |
| 5              | 0101          | F    |
| 6              | 0110          | F♯/G♭ |
| 7              | 0111          | G    |
| 8              | 1000          | G♯/A♭ |
| 9              | 1001          | A    |
| 10             | 1010          | A♯/B♭ |
| 11             | 1011          | B    |
