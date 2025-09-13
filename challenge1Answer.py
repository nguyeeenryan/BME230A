import sys
import numpy

"""The following uses Python to challenge you to create an algorithm for finding
matches between a set of aligned strings. Minimal familiarity with Python is 
necessary, notably list and Numpy array slicing. 

Do read the accompanying Durbin et al. paper before attempting the challenge!
"""

"""Problem 1.

Let X be a list of M binary strings (over the alphabet { 0, 1 }) each of length 
N. 

For integer 0<=i<=N we define an ith prefix sort as a lexicographic sort 
(here 0 precedes 1) of the set of ith prefixes: { x[:i] | x in X }.
Similarly an ith reverse prefix sort is a lexicographic sort of the set of
ith prefixes after each prefix is reversed.

Let A be an Mx(N+1) matrix such that for all 0<=i<M, 0<=j<=N, A[i,j] is the 
index in X of the ith string ordered by jth reverse prefix. To break ties 
(equal prefixes) the ordering of the strings in X is used. 

Complete code for the following function that computes A for a given X.

Here X is a Python list of Python strings. 
To represent A we use a 2D Numpy integer array.

Example:

>>> X = getRandomX() #This is in the challenge1UnitTest.py file
>>> X
['110', '000', '001', '010', '100', '001', '100'] #Binary strings, M=7 and N=3
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> 

Hint:
Column j (0 < j <= N) of the matrix can be constructed from column j-1 and the 
symbol in each sequence at index j-1.  

Question 1: In terms of M and N what is the asymptotic cost of your algorithm?

   > The cost is O(M*N) as it does a single pass through the input  using two for-loops.
"""

def constructReversePrefixSortMatrix(X):
    #Creates the Mx(N+1) matrix
    A = numpy.empty(shape=[len(X), 1 if len(X) == 0 else len(X[0])+1 ], dtype=int) 
    
    #Code to write - you're free to define extra functions 
    #(inline or outside of this function) if you like.

    A[:,0] = [i for i in range(len(X))] #set first column to 0:N-1
    M = len(X) # number of sequences
    N = len(X[0]) # number of variable sites
    
    for x in range(N): # applies algorithm 1 to all variable sites
        
        # algorithm 1
        a = []
        b = []
        for y in range(M):
            if X[A[y][x]][x] == '0': # if 0
                a.append(A[y][x])
            else:                    # if 1
                b.append(A[y][x])

        A[:,x+1] = a + b # New column a_k+1
    
    return A

"""Problem 2: 

Following on from the previous problem, let Y be the MxN matrix such that for 
all 0 <= i < M, 0 <= j < N, Y[i,j] = X[A[i,j]][j].

Complete the following to construct Y for X. 

Hint: You can either use your solution to constructReversePrefixSortMatrix() 
or adapt the code from that algorithm to create Y without using 
constructReversePrefixSortMatrix().

Question 2: In terms of M and N what is the asymptotic cost of your algorithm?

  > It should also be O(M*N) because of the two for-loops, but if this is a trick question
  > then it's O(2*M*N) because the function for problem 1 is used in here as well.
"""
def constructYFromX(X):
    #Creates the MxN matrix
    Y = numpy.empty(shape=[len(X), 0 if len(X) == 0 else len(X[0]) ], dtype=int)
    
    #Code to write - you're free to define extra functions
    #(inline or outside of this function) if you like.

    A = constructReversePrefixSortMatrix(X)
    M = len(X) # number of sequences
    N = len(X[0]) # number of variable sites

    for j in range(N):
        for i in range(M):
            Y[i,j] = X[ A[i][j] ] [j]


    
    return Y

"""Problem 3.

Y is a transformation of X. Complete the following to construct X from Y, 
returning X as a list of strings as defined in problem 1.
Hint: This is the inverse of X to Y, but the code may look very similar.

Question 3a: In terms of M and N what is the asymptotic cost of your algorithm?
  > The cost should be O(M*N)

Question 3b: What could you use Y for? 
  > Y can be used like the BWT in order to compress and reconstruct these types of
  > structures

Hint: consider the BWT.

Question 3c: Can you come up with a more efficient data structure for storing Y?
  > No, I don't think I could.
"""
def constructXFromY(Y):
    #Creates the MxN matrix
    X = numpy.empty(shape=[len(Y), 0 if len(Y) == 0 else len(Y[0]) ], dtype=int)
    
    #Code to write - you're free to define extra functions
    #(inline or outside of this function) if you like.

    A = numpy.empty(shape=[len(Y), 1 if len(Y) == 0 else len(Y[0])+1 ], dtype=int) 
    M = len(Y)
    N = len(Y[0])

    ## (1) Build the first column of A (i.e. [ i for i in range(M) ], call it A_0

    A[:,0] = [i for i in range(M)] #set first column to 0:N-1

    ## (2) For each column I, 0 through N (exclusive)
    for j in range(N):
        a = []
        b = []
        
        for i in range(M):
            X[A[i][j]][j] = Y[i][j] ## (3) Use A_i and Y_i to build X_i
            
            if Y[i][j] == 0: ## (4) Use A_i and Y_i to build A_i+1
                a.append(A[i][j])
            else:
                b.append(A[i][j])
        A[:,j+1] = a + b # New column a_k+1
    
    return ["".join([str(j) for j in i]) for i in X] #Convert back to a list of strings

"""Problem 4.

Define the common suffix of two strings to be the maximum length suffix shared 
by both strings, e.g. for "10110" and "10010" the common suffix is "10" because 
both end with "10" but not both "110" or both "010". 

Let D be a Mx(N+1) Numpy integer array such that for all 1<=i<M, 1<=j<=N, 
D[i,j] is the length of the common suffix between the substrings X[A[i,j]][:j] 
and X[A[i-1,j]][:j].  

Complete code for the following function that computes D for a given A.

Example:

>>> X = getRandomX()
>>> X
['110', '000', '001', '010', '100', '001', '100']
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> D = constructCommonSuffixMatrix(A, X)
>>> D
array([[0, 0, 0, 0],
       [0, 1, 2, 2],
       [0, 1, 2, 3],
       [0, 1, 1, 1],
       [0, 0, 2, 2],
       [0, 1, 0, 0],
       [0, 1, 1, 3]])

Hints: 

As before, column j (0 < j <= N) of the matrix can be constructed from column j-1 
and thesymbol in each sequence at index j-1.

For an efficient algorithm consider that the length of the common suffix 
between X[A[i,j]][:j] and X[A[i-k,j]][:j], for all 0<k<=i is 
min(D[i-k+1,j], D[i-k+2,j], ..., D[i,j]).

Question 4: In terms of M and N what is the asymptotic cost of your algorithm?
  > The algorithm in the book should have a time complexity of O(MN), but
  > I can't get this problem to work so really the time complexity is O(NEVER)
"""
#A4: O(MN)

def constructCommonSuffixMatrix(A, X):
    D = numpy.zeros(shape=A.shape, dtype=int) #Creates the Mx(N+1) D matrix 

    #Code to write - you're free to define extra functions 
    #(inline or outside of this function) if you like.
    M = len(X) # number of sequences
    N = len(X[0]) # number of variable sites
    
    for j in range(N):
        a = []
        b = []
        d = []
        e = []
        p = q = j + 1
        
        for i in range(M):
            
            
            sequence = X[i]
            site = X[j]
            
            match_start = D[i,j]
            
            if match_start > p:
                p = match_start
            if match_start > q:
                q = match_start
            if site == 0:
                a.append(i)
                e.append(q)
                p = 0
            else:
                b.append(i)
                e.append(q)
                q = 0
        A[:,j+1] = a + b
        D[:,j+1] = d + e
    
    return D

"""Problem 5.
    
For a pair of strings X[x], X[y], a long match ending at j is a common substring
of X[x] and X[y] that ends at j (so that X[x][j] != X[y][j] or j == N) that is longer
than a threshold 'minLength'. E.g. for strings "0010100" and "1110111" and length
threshold 2 (or 3) there is a long match "101" ending at 5.
    
The following algorithm enumerates for all long matches between all substrings of
X, except for simplicity those long matches that are not terminated at
the end of the strings.
    
Question 5a: What is the asymptotic cost of the algorithm in terms of M, N and the
number of long matches?
  > O(max(NM, # of matches)) according to the text

Question 5b: Can you see any major time efficiencies that could be gained by
refactoring?
  > Instead of using functions for A and D outside the loop we could integrate
  > it inside the loop like in problem 3
    
Question 5c: Can you see any major space efficiencies that could be gained by
refactoring?
  > It might be possible to use some

Question 5d: Can you imagine alternative algorithms to compute such matches?,
if so, what would be the asymptotic cost and space usage?
  > According to the paper's discussion section, hash functions could
  > be faster with the right adjustment, although they would take more
  > space. Hash tables normally have an asymptotic cost and space usage
  > of O(N) at worst.

"""
def getLongMatches(X, minLength):
    assert minLength > 0
    
    A = constructReversePrefixSortMatrix(X)
    D = constructCommonSuffixMatrix(A, X)
    
    #For each column, in ascending order of column index
    for j in range(1, 0 if len(X) == 0 else len(X[0])):
        #Working arrays used to store indices of strings containing long matches
        #b is an array of strings that have a '0' at position j
        #c is an array of strings that have a '1' at position j
        #When reporting long matches we'll report all pairs of indices in b X c,
        #as these are the long matches that end at j.
        b, c = [], []
        
        #Iterate over the aligned symbols in column j in reverse prefix order
        for i in range(len(X)):
            #For each string in the order check if there is a long match between
            #it and the previous string.
            #If there isn't a long match then this implies that there can
            #be no long matches ending at j between sequences indices in A[:i,j]
            #and sequence indices in A[i:,j], thus we report all long matches
            #found so far and empty the arrays storing long matches.
            if D[i,j] < minLength:
                for x in b:
                    for y in c:
                        #The yield keyword converts the function into a
                        #generator - alternatively we could just to append to
                        #a list and return the list
                        
                        #We return the match as tuple of two sequence
                        #indices (ordered by order in X) and coordinate at which
                        #the match ends
                        yield (x, y, j) if x < y else (y, x, j)
                b, c = [], []
            
            #Partition the sequences by if they have '0' or '1' at position j.
            if X[A[i,j]][j] == '0':
                b.append(A[i,j])
            else:
                c.append(A[i,j])
        
        #Report any leftover long matches for the column
        for x in b:
            for y in c:
                yield (x, y, j) if x < y else (y, x, j)
