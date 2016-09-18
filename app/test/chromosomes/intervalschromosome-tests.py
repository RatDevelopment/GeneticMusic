#------------------------------------------------------------------------------
# File: intervalschromosome-tests.py
# Desc: Interval Chromosome tests
# Auth: Cezary Wojcik
# Date: September 17, 2016
#------------------------------------------------------------------------------

import unittest
from app.src.chromosomes.intervalschromosome import IntervalChromosome

class IntervalsChromosomeTests(unittest.TestCase):

  def test_init(self):
    sequence = 0b10101
    sample_chromosome = IntervalChromosome(sequence)
    self.assertTrue(sample_chromosome.sequence == sequence)

if __name__ == "__main__":
  unittest.main()
