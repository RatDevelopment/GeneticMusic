# Intervals Chromosome

The purpose of this chromosome will essentially be to define a _key_ generator
of sorts. For any given starting note, this chromosome will define the other
possible notes based on offsets from the original note. Each of these possible
notes will have an associated probability of occurence.

## Chromosome Structure

Our chromosome will be divided into chunks that first define an interval in
half steps and then define a number of significance that will be used to
determine the probability for each note.

We will determine the number of half steps by counting the number of `0`s until
we hit a `1`. The number of of half steps will be the number of `0`s plus one.

After we hit a one, we will read the next 4 bits and take them to be the number
of significance for the note following the interval.

Since the number of notes is equal to the number of intervals plus one, we will
begin the sequence with 4 bits that will define the significance for the
starting note, whatever it may be.

### Example

Suppose we have the following sequence:

```
100010101010111
```

We begin parsing by taking the first four bits, `1000` (8). This will be the
significance number for the first note.

We continue parsing by counting the number of `0`s until we hit a `1`. We hit a
`1` right away, so that number is zero. Our first interval, therefore, is zero
plus one halfstep, i.e. just a halfstep. Now, we look at the next four bits in
the sequence to determine the significance number. We see `0101`, which is
5. Therefore, the note after the first interval (i.e. the second note) will
have significance 5.

We count the number of `0`s until we hit a `1` again. This time, we find one
zero, so the number of half steps for this interval will be one plus one, i.e.
two half steps or one whole step. We then look at the next four bits to find
the significance number - we find `0111`, or 7.

So, in separated chunks, we can visualize the above sequence like this:

| Interval Definition  | Significance Number |
|----------------------|---------------------|
|                      | `1000`              |
| `1`                  | `0101`              |
| `01`                 | `0111`              |

Once we have the significance numbers, we can determine the percent probability
for each note to occur by summing the significance numbers and finding dividing
the significance number by the sum. For the example above, we have:

```
0b1000 + 0b0101 + 0b0111 = 8 + 5 + 7 = 20
```

Thus, our final result is:

| Half-steps from starting note | Percentage     |
|-------------------------------|----------------|
| `0`                           | `8 / 20 = 40%` |
| `0 + 1 = 1`                   | `5 / 20 = 25%` |
| `0 + 1 + 2 = 3`               | `7 / 20 = 35%` |

## Junk Genes

There are two main conditions that cause us to begin ignoring genes:

- If the total number of cumulative intervals exceeds ten half-steps, we will
  ignore any additional genes.
- If there are not four genes to define a significance number after an interval
  definition, that interval will be ignored.
