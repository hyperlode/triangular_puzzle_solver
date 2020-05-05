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

    def get_combined_bounding_box(self, patterns):
        bounding_box = self.get_bounding_box(patterns[0])
        for pattern in patterns[1:]:
            
            extra_bounding_box  = self.get_bounding_box(pattern)
            bounding_box = { k:(v if  v > bounding_box[k] else bounding_box[k]) for k,v in extra_bounding_box.items()}
        return bounding_box

    def get_meta_data(self, pattern):
        meta = {}
        meta.update(self.get_bounding_box(pattern))

        # rows_count = max_r - min_r + 1
        # cols_count = max_c - min_c + 1
        # meta.update( { "rows_count":rows_count, "cols_count":cols_count})
        return meta
    
    def get_bounding_box(self, pattern, predefined_dict=None):
        # predefined dict already has all the keys populated with values.

        if predefined_dict is None:
            min_c = None
            min_r = None
            max_c = None
            max_r = None
        else:
            min_c = predefined_dict["min_c"]
            min_r = predefined_dict["min_r"]
            max_c = predefined_dict["max_c"]
            max_r = predefined_dict["max_r"]

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
        
    def mirror(self, pattern, horizontal_else_vertical=True):
        
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
       

        return mirrored

    def translate(self, pattern, direction, steps):


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

        if degrees not in [0,60,120,180,240,300]:
            print("degress has to be in [0,60,120,180,240,300]range")
            raise NonValidDegreesException

        iterations = int(degrees / 60)

        rotation_cell_remap = transformation_CCW
        if cw_else_ccw:
            rotation_cell_remap = transformation_CW

        for i in range(iterations):
            transformed = {}
            print(i)
          
            for cell in pattern:
                transformed[ rotation_cell_remap[cell] ] = pattern[cell]
            pattern = copy.deepcopy(transformed)
        return transformed
        



