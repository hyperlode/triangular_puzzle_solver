import itertools
from pathlib import Path

# all pieces indeces
pieces = [0,1,2,3,4,5,6,7,8,9,10,11]

# all used pieces indeces
used_pieces = [1,2,3,4,5,6,7,8,9,10,11]
# used_pieces = [1,3,4,11]

# board indeces 
boards = ['a','b','c','d','e']

BASE_PATH = r"C:\temp\haley_puzzle"
JOB_NAME = "haley_test.txt"

Path(BASE_PATH).mkdir(parents=True,exist_ok=True)
jobpath = Path(BASE_PATH, JOB_NAME)

class PermutationAsString:
    def __init__(self, elements, variations=None):
        # will return permutation of all pieces for every variation. 
        # arguments should be lists. Lists should not be empty.  elements list should be small, as permutations go faculty skyrocketting high. anything more than 10 elements is in the danger zone.

        self.elements = elements
        self.permutations_sequences = itertools.permutations(elements)
        
        self.variations = variations
        self.variation_index = 0

        if self.variations is not None:
            self.variation = self.variations[self.variation_index]

    def __iter__(self):
        return self

    def __next__(self): # Python 2: def next(self)

        try:
            s = next(self.permutations_sequences)

        except StopIteration:
            if self.variations is None:
                raise StopIteration

            # if multiple variations enable next variation and restart iterator
            self.permutations_sequences = itertools.permutations(self.elements)
            self.variation_index += 1
            if self.variation_index >= len(self.variations):
                raise StopIteration
            self.variation = self.variations[self.variation_index]
            s = next(self.permutations_sequences)
        
        if self.variations is None:
            return "{}".format(",".join(str(i) for i in s))

        else:
            return "{},{}".format(self.variation, ",".join(str(i) for i in s))

def all_permutations_to_file(filePath, elements, variations):

    piter = PermutationAsString (elements, variations)
    with open(filePath,"w") as f:
        # for i in range(100000):

            # s = next(piter)
        for s in piter:
            f.write("{}\n".format(s))

if __name__ == "__main__":
    # all_permutations_to_file(jobpath, used_pieces, boards)
    piter = PermutationAsString ([12,3,4,5])
    for p in piter:
        print(p)
