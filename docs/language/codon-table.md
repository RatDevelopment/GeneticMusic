# Codon Table (Quick Reference)

6-bit codons. Pairs marked (syn) are **synonymous** — mutations between them
change DNA but not the decoded amino acid.

## Special

| Codon | AA |
|-------|-----|
| `000000` / `000001` (syn) | STOP |
| `111110` / `111111` (syn) | NOP |

## Amino acids

| Codons (syn pairs) | Amino acid | Parameter (typical) |
|--------------------|------------|---------------------|
| `001000` / `001001` | DEGREE | scale degree 0–7 |
| `001010` / `001011` | DEGREE_OFF | degree + chromatic offset |
| `001100` / `001101` | REST | duration ticks |
| `001110` / `001111` | HOLD | — |
| `010000` / `010001` | REPEAT_LAST | count |
| `010010` / `010011` | MOTIF_REF | motif id 0–15 |
| `010100` / `010101` | DUR | rhythm class |
| `010110` / `010111` | DUR_DOT | rhythm class |
| `011000` / `011001` | DUR_TRIPLET | rhythm class |
| `011010` / `011011` | STACCATO | gate % |
| `011100` / `011101` | FERMATA | — |
| `011110` / `011111` | CHORD_DEG | degree set / chord type |
| `100000` / `100001` | ARP_UP | — |
| `100010` / `100011` | ARP_DOWN | — |
| `100100` / `100101` | TRANSPOSE | ± semitones |
| `100110` / `100111` | INVERT | axis pitch |
| `101000` / `101001` | VELOCITY | 0–127 |
| `101010` / `101011` | PROGRAM | GM program |
| `101100` / `101101` | CC | controller + value |
| `101110` / `101111` | OCTAVE_SHIFT | ±1 octave |
| `110000` / `110001` | SECTION | marker id |
| `110010` / `110011` | COPY_PROTEIN | src id + range |
| `110100` / `110101` | MUTATE_RATE | local rate |
| `110110` / `110111` | REVERSE | length N |

Unassigned codons in `110xxx`–`111101` decode as **NOP** until specified.

## Note names in parameter codons

When a parameter encodes absolute pitch class, use the [note
mapping](../overview.md) (4 bits, `0000` = C … `1011` = B).
