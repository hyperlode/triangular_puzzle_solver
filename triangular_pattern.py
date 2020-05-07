import copy

# will rotate all cells 60 degrees ccw, around bottom right corner of cell (0,0)
# hard coded --> was easier than finding a formula. limited piece size!
# all cells for a hexgon with side size = 3 cells available.


TRANSLATE_DIRECTIONS = {
    "E":(2,0),
    "W":(-2,0),
    "NE":(1,-1),
    "SE":(1,1),
    "NW":(-1,-1),
    "SW":(-1,1),
    "S":(0,2),
    "N":(0,-2),

}
DIRECTIONS_NAME = ["NE","SE","NW","SW","E","W", "N", "S"]

transformation_CCW = {
    (0,0):(1,0),
    (1,0):(1,1),
    (1,1):(1,2),
    (1,2):(0,2),
    (0,2):(0,1),
    (0,1):(0,0),

    (0,-1):(1,-1),
    (1,-1):(2,1),
    (2,1):(1,3),
    (1,3):(0,3),
    (0,3):(-1,1),
    (-1,1):(0,-1),

    (0,-2):(2,-1),
    (2,-1):(2,2),
    (2,2):(1,4),
    (1,4):(-1,3),
    (-1,3):(-1,0),
    (-1,0):(0,-2),

    (-1,-1):(1,-2),
    (1,-2):(2,0),
    (2,0):(2,3),
    (2,3):(0,4),
    (0,4):(-1,2),
    (-1,2):(-1,-1),
    
    (0,-4):(3,-2),
    (3,-2):(3,3),
    (3,3):(1,6),
    (1,6):(-2,4),
    (-2,4):(-2,-1),
    (-2,-1):(0,-4),

    (0,-3):(2,-2),
    (2,-2):(3,2),
    (3,2):(1,5),
    (1,5):(-1,4),
    (-1,4):(-2,0),
    (-2,0):(0,-3),

    (-1,-3):(2,-3),
    (2,-3):(3,1),
    (3,1):(2,5),
    (2,5):(-1,5),
    (-1,5):(-2,1),
    (-2,1):(-1,-3),

    (-1,-2):(1,-3),
    (1,-3):(3,0),
    (3,0):(2,4),
    (2,4):(0,5),
    (0,5):(-2,2),
    (-2,2):(-1,-2),

    (-2,-2):(1,-4),
    (1,-4):(3,-1),
    (3,-1):(3,4),
    (3,4):(0,6),
    (0,6):(-2,3),
    (-2,3):(-2,-2),
}

transformation_CW = {v: k for k, v in transformation_CCW.items()}

class TriangularPatternOperations():
    # has no edge cases.
    # 0,0 is always an up facing triangle.  /\

    def __init__(self):
        pass
        # self._cells = copy.deepcopy(cells)

    def delete_equal_patterns(self, patterns):
        # patterns is a list of patterns. (each pattern is a dict)
        # will only delete pattersn with exact same orientations!
        # so, mirrored and rotated are differentiated,
        #return [dict(t) for t in {tuple(d.items()) for d in patterns}]  # https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python

        filtered = []
        for p in patterns:
            equal_found = False
            for f in filtered:
                if p == f:
                    equal_found = True
            if not equal_found:
                filtered.append(p)
        return filtered


    def crop_pattern_to_bounding_box(self, pattern):
        # play it save, use "normalize"
        # assume all coordinates are positive. (if not, use normalize)
        bb = self.get_bounding_box(pattern)
        cropped = {}
        

        # this is a little hack, because we cannot just move things around the triagular grid like in a square one. If you move an odd sum of rows and colums, the shape changes!
        rows_even = False
        if bb["min_r"] % 2 == 0:
            # even, no problemo
            rows_even = True
        
        cols_even = False
        if bb["min_c"] % 2 == 0:
            # even, no problemo
            cols_even = True
        
        if (rows_even and cols_even) or (not(rows_even) and not(cols_even)):
            # perfect, move it.
            extra_space = 0
        else:
            # if one (of rows and cols) is even and the other one odd.
            # go against top row, but leave one space on the left side.
            extra_space = 1

        for cell in pattern:
            r,c = cell
            cropped[(r - bb["min_r"] + extra_space, c - bb["min_c"])] = pattern[cell]

        return cropped

    def normalize_pattern(self, pattern):
        # translate to make sure there are no negaive coordinates.
        # move as much to topleft as possible without negative numbers.

        check = True
        while check:
            move_south = False
            move_east = False
            for cell in pattern:
                r,c = cell
                if r < 0:
                    move_south = True
                if c < 0:
                    move_east = True

            if move_south:
                pattern = self.translate(pattern,"S")
                
            if move_east:
                pattern = self.translate(pattern,"E")

            if not move_south and not move_east:
                check = False

        pattern = self.crop_pattern_to_bounding_box(pattern)
        return pattern

    def arrange_patterns_for_no_overlap(self, patterns, patterns_per_arrangement_row):
        # will translate all patterns so that their coordinates do not overlap
        # effectively preparing them to be put spaciously on a grid. 

        arranged_patterns = []

        right_col = 0
        bottom_row = 0
        col_count = 0
        next_bottom_row = 0

        # move pattern to edges.
        for pattern in patterns:
            col_count += 1

            bb = self.get_bounding_box(pattern)

            # check horizontal spacing
            while right_col + 1 >= bb["min_c"]:
                pattern = self.translate(pattern, "E")
                bb = self.get_bounding_box(pattern)
            
            # update boundary
            right_col = bb["max_c"]

            # check vertical spacing
            while bottom_row + 1 >= bb["min_r"]:
                pattern = self.translate(pattern, "S")
                bb = self.get_bounding_box(pattern)
            
            # update boundary
            if bb["max_r"] > next_bottom_row:
                next_bottom_row = bb["max_r"]

            
            if col_count == patterns_per_arrangement_row:
                # next row.
                bottom_row = next_bottom_row

                col_count = 0

                right_col = 0

            arranged_patterns.append(pattern)
        return arranged_patterns


    def get_combined_bounding_box(self, patterns):
        bounding_box = self.get_bounding_box(patterns[0])
        for pattern in patterns[1:]:
            
            extra_bounding_box  = self.get_bounding_box(pattern)
            bounding_box = { k:(v if  v > bounding_box[k] else bounding_box[k]) for k,v in extra_bounding_box.items()}
        return bounding_box

    def get_meta_data(self, pattern):
        meta = {}
        meta.update(self.get_bounding_box(pattern))

        return meta
    
    def get_bounding_box(self, pattern):
        # predefined dict already has all the keys populated with values.

        
        min_c = None
        min_r = None
        max_c = None
        max_r = None
       
        for r,c in pattern.keys():
            if min_r is None or r < min_r:
                min_r = r
            if max_r is None or r > max_r:
                max_r = r
            if min_c is None or c < min_c:
                min_c = c
            if max_c is None or c > max_c:
                max_c = c
       
        return {"min_c":min_c, "min_r":min_r, "max_c":max_c, "max_r":max_r}
        
    def mirror(self, pattern, horizontal_else_vertical=True, crop=False):
        
        # search for mirror parameters.
        meta = self.get_bounding_box(pattern)

        mirrored = {}
       
        if horizontal_else_vertical:
            
            for cell in pattern.keys():
                r,c = cell
                # mirrored[r , c + 1] = pattern[cell]
                horizonal_offset = 2 * (meta["max_c"] - c) + 2
                mirrored[r , c + horizonal_offset ] = pattern[cell]
        else:
            for cell in pattern.keys():
                r,c = cell
                vertical_offset = 2 * (meta["max_r"] - r) + 1
                mirrored[r + vertical_offset , c ] = pattern[cell]
                # mirrored[r , c + 1 ] = pattern[cell]  # yes, col + 1 to mirror vertically. 
       
        if crop:
            mirrored = self.normalize_pattern(mirrored)

        return mirrored

    def translate(self, pattern, direction, steps=1):


        if direction not in DIRECTIONS_NAME:
            print("degress has to be in :{}".format(DIRECTIONS_NAME))
            raise NonValidDegreesException

        steps = int(steps)  # must be integer.

        translated = {}
        
        x, y = TRANSLATE_DIRECTIONS[direction]
        
        # number of steps.
        x*= steps
        y*= steps

        for cell in pattern.keys():
            r,c = cell
            translated[r + y, c + x] = pattern[cell]
        
        return translated

    
    def rotate(self, pattern, degrees, cw_else_ccw):
        # will return normalize pattern. = minimum bounding box and no negatives.

        if degrees not in [0, 60,120,180,240,300,360]:
            print("degress has to be in [0,60,120,180,240,300]range")
            raise NonValidDegreesException
        
        # bit of a silly hack. 
        if degrees == 0:
            degrees = 360

        iterations = int(degrees / 60)

        rotation_cell_remap = transformation_CCW
        if cw_else_ccw:
            rotation_cell_remap = transformation_CW

        # rotate multiple times to reach required rotation.
        for _ in range(iterations):
            transformed = {}
            
            for cell in pattern:
                transformed[ rotation_cell_remap[cell] ] = pattern[cell]
            pattern = copy.deepcopy(transformed)

        transformed = self.normalize_pattern(transformed)
        return transformed
        



