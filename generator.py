import random
from PIL import Image, ImageDraw, ImageFont
import math

def main(word_list:list, num:int, width:int, height:int, word_count:int, attempt:int):
    attempt+= 1
    total_words= []
    for i in word_list:
        total_words.append(i)
    words = []
    directions = ["vertical","diagonal-up","horizontal","diagonal-down"]
    reverse = [-1,1]
    max_length = min(width,height)

    letter_count = 0

    for i in range(word_count):
        word_added = False
        while not word_added:
            word_selected = random.randint(0,len(total_words)-1)
            if len(total_words[word_selected]) < max_length and len(total_words[word_selected]) >3: # minimum word length: 4
                letters = list(total_words[word_selected])
                letter_count += len(letters)
                words.append(total_words[word_selected].lower())
                total_words.remove(total_words[word_selected])
                word_added = True

    word_grid = []
    row = []
    for i in range(width):
        for j in range(height):
            row.append(".")
        word_grid.append(row)
        row = []



    dir = ""
    word_letters = []
    co_ord= []

    # place words
    failed = False
    for i in words:
        attempts = 0
        place = False
        word_letters = list(i)
        dir_mult=[0,0]
        reverse_dir = random.choice(reverse)
        
        while not place:
            attempts += 1
            valid = True
            dir = random.choice(directions)
            co_ord = [random.randint(0,width-1) ,random.randint(0,height-1)]

            if (word_grid[co_ord[0]][co_ord[1]] == "." or word_grid[co_ord[0]][co_ord[1]] == word_letters[0]) and attempts <= width*height*len(words):

                if dir == "horizontal":
                    dir_mult = [1*reverse_dir,0]
                elif dir == "diagonal-up":
                    dir_mult = [1*reverse_dir,1*reverse_dir]
                elif dir == "diagonal-down":
                    dir_mult = [-1*reverse_dir,1*reverse_dir]
                elif dir == "vertical":
                    dir_mult = [0,1*reverse_dir]

                word_len = len(word_letters)
                end_row = co_ord[0] + (word_len - 1) * dir_mult[0]
                end_col = co_ord[1] + (word_len - 1) * dir_mult[1]
                attempts += 1
                if (0 <= end_row < width) and (0 <= end_col < height):
                    count = 0
                    for letter in word_letters:
                        new_cord = [co_ord[0]+count*dir_mult[0],co_ord[1]+count*dir_mult[1]]
                        if word_grid[new_cord[0]][new_cord[1]] == "." or word_grid[new_cord[0]][new_cord[1]] == word_letters[count]:
                            valid = True                            
                        else:
                            valid = False
                            break
                        count += 1
                    
                    if valid:
                        attempts = 0
                        count = 0
                        for letter in word_letters:
                            new_cord = [co_ord[0] + count * dir_mult[0], co_ord[1] + count * dir_mult[1]]
                            word_grid[new_cord[0]][new_cord[1]] = letter
                            count += 1
                        place = True
            elif attempts >= width*height*len(words):
                place = True
                failed = True
            if failed: # this may be bad code practice... 0_0
                break
        if failed:
            break
            
    if failed and attempt < 100: # fail safe recursion
       main(word_list,num,width,height,word_count,attempt)
    elif attempt >= 100: # admits failiure after 100 tries
         print("image generation failed.")
    else:
        letters = "abcdefghijklmnopqrstuvwxyz"
        #letters = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
        letter_list = list(letters)

        row_selected = -1
        column_selected = -1

        for i in range(width):
            row_selected += 1
            for j in range(height):
                if word_grid[row_selected][column_selected] == ".":
                    word_grid[row_selected][column_selected] = random.choice(letter_list)
                column_selected += 1
            column_selected = -1



        # for i in range(width):
        #     print(word_grid[i])


        # create image
        cell_size = 50  # pixels per square
        padding = 3
        grid_color = (40, 40, 40)
        image_width = cell_size*width + padding*width + padding

        top_margin = 120   # space for "WORDS:" header
        bottom_margin = 20
        image_height = cell_size*height + padding*height + padding + top_margin + bottom_margin + math.ceil(word_count / max(1, width // 5)) * cell_size

        # define image and draw it
        image = Image.new("RGB", (image_width, image_height), color=grid_color)
        draw = ImageDraw.Draw(image)


        # working with the font
        try:
            font = ImageFont.truetype("fonts/Gaegu-Regular.ttf", 40)
        except IOError:
            font = ImageFont.load_default(size=40)
        try:
            font2 = ImageFont.truetype("fonts/Aller_Bd.ttf", 45)
        except IOError:
            font2 = ImageFont.load_default(size=45)

        counter = 0
        for row in range(height):
            for col in range(width):
                counter += 1
                # create cell dimentions
                x1 = (col * cell_size) + ((col + 1) * padding)
                y1 = (row * cell_size) + ((row + 1) * padding)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if (row+col) % 2 == 0:
                    cell_color = (210,210,210)
                else:
                    cell_color = (245,245,245)

                midpoint_x = x1 + cell_size/2
                midpoint_y = y1 + cell_size/2
                draw.rectangle([x1, y1, x2, y2], fill=cell_color)

                draw.text(
                    (midpoint_x, midpoint_y),
                    word_grid[col][row],
                    fill=(40, 40, 40),
                    font=font,
                    anchor="mm"
                )

        draw.rectangle([padding,
                        cell_size*height + padding*height + padding,
                       image_width-padding,
                        image_height-padding],
                       fill=(220,190,200))

        x3 = 20
        y3 = cell_size*height + padding*height + padding + 70

        draw.text(
                        (x3-5, y3-55),
                        "WORDS:",
                        fill=(40, 40, 40),
                        font=font2,
                        anchor="lt"
                    )

        counter2 = 0
        for word in words:
            row_count = max(1,width // 5)
            counter2 += 1
            current_size = max(10, 45 - len(word))
            try:
                font = ImageFont.truetype("fonts/Gaegu-Regular.ttf", current_size)
            except IOError:
                font = ImageFont.load_default(size=current_size)
            
            draw.text(
                        (x3 + image_width/row_count*(counter2%row_count), y3),
                        word,
                        fill=(40, 40, 40),
                        font=font,
                        anchor="lt"
                        )
            if counter2 % row_count == 0:
                    y3 += cell_size


        # save image
        image.save(f"output/letter_grid{num}.png")
        print("grid image successfully created!")

#settings
amount_wanted = 1
width = 20
height = 20
words = 18

word_list = []

total_letters = 0
average_word_length = 0
word_count = 0
        
with open("word_list/english3.txt") as f:
        for word in f:
            word_count += 1
            total_letters += len(list(word))
            word_list.append(word.strip())

average_word_length = total_letters/word_count

if round(average_word_length*words) > width*height-width-height:
        print("WARNING: word generation may have trouble.")
        
for i in range(amount_wanted):
    main(word_list,i,width,height,words,0)

