# Protein–Codon Musical Language

This document defines a **genetic language** for GeneticMusic: DNA-like
sequences that decode to MIDI, and that remain stable under **selection**,
**crossover**, and **mutation**. It extends the existing [chromosome
model](../overview.md) and composes with the [intervals
chromosome](../chromosomes/intervals-chromosome.md).

## Design goals

| Goal | Implication |
|------|-------------|
| Evolvable offspring | Crossover cuts on **codon** or **protein** boundaries, not arbitrary bits |
| Meaningful mutations | Most small edits change **local** musical meaning, not the whole piece |
| Neutral variation | Multiple codons map to the **same** amino acid (synonymous codons) |
| Composable genome | Several independent **proteins** (voices, harmony, rhythm, regulation) |
| MIDI as phenotype | Decode → event list → MIDI file/track; fitness runs on the **rendered** output |

Biology is the metaphor, not the implementation constraint: we optimize for
**genetic operators**, not biochemical realism.

---

## Hierarchy

```
Genome
├── Regulatory region     (key, scale, probabilities — e.g. intervals chromosome)
├── Protein A             (e.g. melody voice)
│   └── Amino acid*
├── Protein B             (e.g. bass / harmony)
│   └── Amino acid*
└── Global parameters     (tempo, time signature, program change)
```

| Level | Unit size | Role |
|-------|-----------|------|
| **Nucleotide** | 2 bits | Quaternary symbol `A,C,G,T` (optional; groups into codons) |
| **Codon** | 6 bits (3 nucleotides) | Smallest **heritable** word; target of point mutation |
| **Amino acid** | 1 codon → semantic op | One musical “instruction” with opcode + operands |
| **Protein** | Variable-length AA chain | One coherent musical function (melody, drums, harmony) |
| **Genome** | Fixed header + proteins + stop | Full individual; one MIDI score |

**Phenotype** = render(genome) → ordered MIDI events (note on/off, CC, tempo).

**Fitness** = function(phenotype, optional human score). Selection operates on
genomes; only phenotypes are heard.

---

## Binary layout (GA-friendly)

All heritable data is a **bit string**. Parsing is deterministic and
**alignment-sensitive**: crossover and mutation should preserve codon alignment
(multiples of 6 bits in coding regions).

### Genome header (fixed 32 bits)

| Field | Bits | Encoding |
|-------|------|----------|
| Chromosome / genome version | 4 | Schema id for forward compatibility |
| Tempo (BPM) | 8 | `60 + value` (60–315 BPM) |
| Time signature | 4 | Enum: 4/4, 3/4, 6/8, 2/4, 5/4, … |
| Ticks per beat (MIDI division) | 4 | Enum: 480, 240, 96, … |
| Default program (instrument) | 7 | General MIDI 0–127 |
| Reserved | 5 | Must be 0 |

### Regulatory region

Embed or reference the existing **intervals chromosome**: starting-note
weights and half-step intervals define a **pitch distribution** used whenever
an amino acid says “choose pitch from key.”

Keep it as a **separate substring** with its own parser so crossover can:

- swap melody protein while keeping key regulation, or
- swap regulation while keeping rhythmic protein.

### Protein block

Each protein:

| Field | Bits | Meaning |
|-------|------|---------|
| Protein type id | 4 | Melody, bass, chord pad, percussion, FX, … |
| Channel | 4 | MIDI channel 0–15 |
| Length in codons | 8 | Number of codons following (max 255 per protein) |
| Codon × N | 6N | Amino acid sequence |
| Stop codon | 6 | `000000` — end of this protein |

Genome ends with **genome stop** `000000` after the last protein.

**Crossover sites**: between proteins, or between codons inside one protein
(preferred for melody). **Do not** split a codon.

---

## Codon → amino acid (genetic code)

64 codons (6 bits). **48 codons** encode **24 amino acids** (2 synonymous
codons each); **4** are **stop**; **12** are **non-coding / junk** that decode
as no-ops (padding for insert mutations without breaking frame).

Synonymy example: `000000` and `000001` both → **REST**.

### Stop and control

| Codon (6 bits) | Symbol | Effect |
|----------------|--------|--------|
| `000000` | STOP | End protein |
| `000001` | STOP_ALT | Synonymous stop (same) |
| `111111` | NOP | No-op (neutral mutation target) |
| `111110` | NOP_ALT | No-op |

### Pitch / melody (use regulatory intervals for actual pitch)

| Codon | AA | Operands (from same or next codon) | MIDI effect |
|-------|-----|--------------------------------------|-------------|
| `001000`–`001001` | DEGREE | scale degree 0–7 in next codon’s low 3 bits | Note from key |
| `001010`–`001011` | DEGREE_OFF | degree + chromatic offset | Note outside scale |
| `001100`–`001101` | REST | length in ticks (parameter codon) | Silence |
| `001110`–`001111` | HOLD | extends previous note | Tie / longer duration |
| `010000`–`010001` | REPEAT_LAST | count | Repeat previous pitch/rhythm |
| `010010`–`010011` | MOTIF_REF | motif id 0–15 | Play stored motif fragment |

### Rhythm / duration

Duration is in **ticks** (from header division). Parameter codons use **4-bit
rhythm class + 4-bit multiplier** in an 8-bit extension codon when needed.

| Codon | AA | Meaning |
|-------|-----|---------|
| `010100`–`010101` | DUR | Set default note length (eighth, quarter, …) |
| `010110`–`010111` | DUR_DOT | Dotted variant |
| `011000`–`011001` | DUR_TRIPLET | Triplet variant |
| `011010`–`011011` | STACCATO | Shorten last note (gate %) |
| `011100`–`011101` | FERMATA | Hold past written duration |

### Harmony / texture

| Codon | AA | Meaning |
|-------|-----|---------|
| `011110`–`011111` | CHORD_DEG | Stack scale degrees (triad, seventh) |
| `100000`–`100001` | ARP_UP | Arpeggiate last chord up |
| `100010`–`100011` | ARP_DOWN | Arpeggiate down |
| `100100`–`100101` | TRANSPOSE | ± semitones (signed nibble) |
| `100110`–`100111` | INVERT | Invert contour around axis pitch |

### Expression / orchestration

| Codon | AA | Meaning |
|-------|-----|---------|
| `101000`–`101001` | VELOCITY | Set note velocity |
| `101010`–`101011` | PROGRAM | Change instrument |
| `101100`–`101101` | CC | Control change (mod, sustain, …) |
| `101110`–`101111` | OCTAVE_SHIFT | Shift register ±1 octave |

### Form / higher-level (motifs in genome library)

| Codon | AA | Meaning |
|-------|-----|---------|
| `110000`–`110001` | SECTION | Marker for fitness segmentation |
| `110010`–`110011` | COPY_PROTEIN | Duplicate another protein’s segment |
| `110100`–`110101` | MUTATE_RATE | Local hypermutation zone (evo meta) |
| `110110`–`110111` | REVERSE | Retrograde last N amino acids |

Junk codons (`110000`–`111101` not in table) → **NOP** until assigned.

---

## Operand extension (optional second codon)

Simple amino acids pack parameters into the **same** 6 bits (2-bit opcode
class + 4-bit immediate). Richer ops consume **two codons**:

1. **Opcode codon** — selects amino acid.
2. **Parameter codon** — pitch class, duration ticks, velocity, degree, etc.

The renderer maintains a **cursor**; if an opcode expects a parameter and the
next codon is STOP, treat as “default parameter” (weak semantics, survives
mutation).

This mirrors prokaryotic **overlapping genes**: fixed frame, variable arity.

---

## Mapping to MIDI (phenotype pipeline)

```
genome bits
  → parse header & regulatory (intervals)
  → for each protein:
        state = { channel, last_pitch, default_dur, velocity, … }
        for each amino acid:
            emit 0+ MIDI events into track[channel]
  → merge tracks, apply tempo map
  → write .mid / play via synthesizer
```

**Note amino acids** do not store absolute pitch unless using `DEGREE_OFF`;
they call `sample_pitch(regulatory_intervals, degree)` so the same melody
DNA sounds different in different keys — regulation and melody **coevolve**.

Suggested defaults:

- Note on: `0x90`, velocity from state, duration from `DUR` + ticks.
- Note off: `0x80` or note-on with duration for simpler library code.
- Percussion protein type: degree maps to **General MIDI drum** map.

---

## Genetic operators

### Selection

- **Human**: listen to N renders, rank or tournament pick.
- **Automatic** (optional): target interval consonance, rhythmic entropy, range,
  repetition penalty. Use only as assist; pure autonomic fitness often converges
  to noise.

### Crossover

| Operator | Where | Effect |
|----------|-------|--------|
| Single-point | Between proteins | Swap voice blocks (melody ↔ melody) |
| Single-point | Between codons | Blend phrases inside one protein |
| Uniform | Per codon | 50% codon from each parent |
| Regulatory swap | Intervals region only | New key/color, same rhythm |

Always **frame-align** (multiple of 6 bits in coding regions).

### Mutation

| Type | Rate (typical) | Effect |
|------|----------------|--------|
| Point (nucleotide) | low | May be synonymous if codon unchanged |
| Codon substitution | medium | Random valid codon; respect protein type |
| Insert codon | low | NOP or duplicate neighbor; shift length field |
| Delete codon | low | Remove; shorten length |
| Protein dup / delete | very low | Structural novelty |
| Regulatory | medium | Intervals/significance bits |

**Synonymous mutations** (e.g. flip one nucleotide in `001000` → `001001`)
preserve phenotype → genetic drift; **nonsynonymous** explore nearby musical
space.

### Elitism

Keep top k genomes unchanged each generation to preserve good motifs.

---

## Relation to existing chromosomes

| Existing concept | Role in this language |
|------------------|------------------------|
| Chromosome designator (4 bits) | Genome version + protein type ids |
| Note gene `0000`–`1011` | Used inside parameter codons or `DEGREE_OFF` |
| Intervals chromosome | **Regulatory region** — pitch statistics |

The intervals chromosome is **not** deprecated; it is the **transcription
factor** for pitch sampling. Melody proteins are **structural** sequences built
from amino acids.

---

## Implementation order

1. **Codon table** + parser (genome → list of typed amino acids).
2. **Renderer** (amino acids + intervals → MIDI event list).
3. **Population** + mutation/crossover on aligned bit strings.
4. **Fitness UI** (play, rate, breed).
5. Motif library (`MOTIF_REF`, `COPY_PROTEIN`) once basic loop works.

---

## Example (conceptual)

Regulatory: C major, degrees 0,2,4 weighted.

Protein (melody): `DEGREE(0) DUR(quarter) DEGREE(2) DEGREE(4) REST(8) STOP`

Phenotype: C4 – E4 – G4 – rest – (MIDI track).

Two parents with crossover after `DEGREE(2)` swap tails → offspring inherits
shared prefix motif, novel suffix — **audible heredity**.
