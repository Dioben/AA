# Rafael Carrascosa's Count-Min Sketch pure python implementation
#
# Adapted from https://github.com/rafacarrascosa/countminsketch
#
# Using delta and epsilon as suggested in https://github.com/AWNystrom/CountMinSketch
#
# J. Madeira --- December 2018
#
# Further Adjustments by Diogo Bento --- January 2021

import math

import numpy as np

class CountMinSketch(object):
    """
    A class for counting hashable items using the Count-min Sketch strategy.

    The Count-min Sketch is a randomized data structure that uses a constant
    amount of memory and has constant insertion and lookup times at the cost
    of an arbitrarily small overestimation of the counts.

    It has two parameters:
     - `m` the size of the hash tables, larger implies smaller overestimation
     - `d` the number of hash tables, larger implies lower probability of
           overestimation.

    Note that this class can be used to count *any* hashable type, so it's
    possible to "count apples" and then "ask for oranges". Validation is up to
    the user.
    """

    def __init__(self, m=None, d=None, delta=None, epsilon=None):
        """
        Parameters
        ----------
        m : the number of columns in the count matrix
        d : the number of rows in the count matrix -> formal language has |rows| hash functions, even if it seems opposite of what's intuitive
        delta : (not applicable if m and d are supplied) the probability of query error
        epsilon : (not applicable if w and d are supplied) the query error factor
        """
        
        #CHANGELOG:
        """
        print statement has been moved to __str__
        table is now numpy based
        """
        if m is not None and d is not None:
            self.m = m
            self.d = d
        elif delta is not None and epsilon is not None:
            # Computing the size of the sketch
            self.m = math.ceil(2.0 / epsilon)
            self.d = math.ceil(math.log(1.0 / delta))
        else:
            raise ValueError( "You must either supply both m and d or delta and epsilon.")
        

        self.n = 0

        self.table = np.zeros((d,m),dtype=np.uint64)

    def _hash(self,x):
        #CHANGELOG: Entirely redone for better readability
        values = []
        for i in range(self.d):
            item = (x,i)
            values.append( abs(hash(item)) % self.m)
        return values
    '''
    def _hash(self, x):
        md5 = hashlib.md5(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
        for i in range(self.d):
            md5.update(str(i).encode("utf-8"))              # concatenate
            yield int(md5.hexdigest(), 16) % self.m
    '''

    def update(self, x):
        """
        Count element `x` as if had appeared `value` times.
        By default `value=1` so:

            sketch.add(x)

        Effectively counts `x` as occurring once.
        """
        #CHANGELOG:
        '''
        removed the value parameter
        changed indexing a bit
        '''
        self.n += 1
        for index in zip( range(self.d) , self._hash(x)):
            self.table[index] += 1

    def query(self, x):
        """
        Return an estimation of the amount of times `x` has ocurred.
        The returned value always overestimates the real value.
        """
        #CHANGELOG: Changed indexing a bit
        return min(self.table[index] for index in zip(range(self.d), self._hash(x)))

    def __getitem__(self, x):
        """
        A convenience method to call `query`.
        """
        return self.query(x)

    def __len__(self):
        """
        The number of things counted. Takes into account that the `value`
        argument of `add` might be different from 1.
        """
        return self.n

    def __str__(self):
            return("CM Sketch with " + str(self.m) + " columns and " + str(self.d) + " rows")