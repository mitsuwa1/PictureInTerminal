import os

# Image
def main(**kwargs):
    negative = False
    if 'negative' in kwargs:
        ng = kwargs["negative"]
    assert kwargs["path"]
    path = kwargs["path"]

    # Image
    from PIL import Image
    global im
    im = (Image.open(path)).convert(mode="L")
    global width, height
    width, height = im.size

    # Cell
    class Cell:
        def __init__(self, w=1, h=1):
            self.w = w
            self.h = h

        @property
        def square(self):
            return self.w*self.h

    terminal_width, terminal_height = os.get_terminal_size()

    cell_width, cell_height = (1,1)
    if width>terminal_width:
        for i in range(1,100000):
            if width//(i)<=terminal_width:
                cell_width, cell_height = (i,cell_height)
                break
    else:
        pass

    if height>terminal_height:
        for i in range(1,100000):
            if height//(i)<=terminal_height:
                cell_width, cell_height = (cell_width,i)
                break
    else:
        pass

    cell = Cell(cell_width, cell_height)

    
    # Picture arr
    RGB_ARR = [i*(256/12) for i in range(1,12+1)]
    SYMBOLS_ARR = ['.',',','-','~',':',';','=','!','*','#','$','@']
    if ng==True:
        SYMBOLS_ARR = SYMBOLS_ARR[::-1]


    def HorizontalCalculation(y_pos=0, current_cell=cell):
        cropped = []
        global im, width, height
        for i in range(1, width//current_cell.w+1):
            x1 = i*current_cell.w - current_cell.w
            y1 = y_pos
            x2 = i*current_cell.w
            y2 = y1+current_cell.h
            coords = (x1,y1,x2,y2)
            im_crop = im.crop(coords)
            cropped.append(im_crop)

        if width//current_cell.w*current_cell.w != width:
            x1 = width//current_cell.w*current_cell.w
            y1 = y_pos
            x2 = width
            y2 = y_pos + current_cell.h
            coords = (x1,y1,x2,y2)
            im_crop = im.crop(coords)
            cropped.append(im_crop)

        return cropped


    def VerticalCalculation(current_cell=cell):
        full_arr = []
        for i in range(1, height//current_cell.h+1):
            line_arr = HorizontalCalculation(y_pos=i*current_cell.h-current_cell.h)
            full_arr.append(line_arr)

        if height//current_cell.h*current_cell.h != height:
            new_cell = Cell(w=current_cell.w, h=height-height//current_cell.h*current_cell.h)
            full_arr.append(HorizontalCalculation(current_cell=new_cell))

        return full_arr
        
    def ColorToValue(num):
        assert num <= 256, "AVG color can't be more than 256"
        
        for i in range(len(RGB_ARR)-1):
            left = RGB_ARR[i]
            right = RGB_ARR[i+1]
            if (left <= num) and (num<= right):
                leftdelta = num-left
                rightdelta = right-num
                if leftdelta<rightdelta:
                    return i+1
                else:
                    return i+2
        return 1

    def ValueToSymbol(num):
        assert 1<=num<=12 and num%1==0, 'Unable to make a symbol - incorrect number'
        return SYMBOLS_ARR[num-1]


    all = VerticalCalculation()

    picture_arr = []
    for line in all:
        line_arr = []
        for zone in line:
            pixels_seq = zone.getdata()
            pixels_count = len(pixels_seq)
            avg_color = sum(x for x in pixels_seq)/pixels_count
            zone_val = ColorToValue(avg_color)
            line_arr.append(ValueToSymbol(zone_val))
        picture_arr.append(line_arr)

    return picture_arr


def Draw(path,*args,**kwargs):
    ng = False
    if 'negative' in kwargs:
        if kwargs['negative']:
            ng = True
        else:
            ng = False
            
    
    for elem in main(path=path, negative=ng):
        line = ''
        for symbol in elem:
            line += symbol
        print(line)
