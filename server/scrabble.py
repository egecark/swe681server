import numpy as np

TRIPLE_WORD_SCORE = [[0,0], [7, 0], [14,0], [0, 7], [14, 7], [0, 14], [7, 14], [14,14]]
DOUBLE_WORD_SCORE = [[1,1], [2,2], [3,3], [4,4], [1, 13], [2, 12], [3, 11], [4, 10], [13, 1], [12, 2], [11, 3], [10, 4], [13,13], [12, 12], [11,11], [10,10]]
TRIPLE_LETTER_SCORE = [[1,5], [1, 9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13, 5], [13,9]]
DOUBLE_LETTER_SCORE = [[0, 3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], [7,3], [7,11], [8,2], [8,6], [8,8], [8, 12], [11,0], [11,7], [11,14], [12,6], [12,8], [14, 3], [14, 11]]

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
points  = [ 1 ,  3 ,  3 ,  2 ,  1 ,  4 ,  2 ,  4 ,  1 ,  8 ,  5 ,  1 ,  3 ,  1 ,  1 ,  3 ,  10,  1 ,  1 ,  1 ,  1 ,  4 ,  4 ,  8 ,  4 ,  10]

points_map = dict(zip(letters, points))

scrabble_values = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", '','2L','2W','3L','3W']

def parse_board(board_string):
    board = np.full(shape=(15,15), fill_value=' ')

    i = 0

    row = 0
    col = 0

    if board_string[0] != '[' or board_string[-1] != ']':
        return False


    while(i < len(board_string) - 1):
        i += 1

        letter = board_string[i]

        if letter == ',':
            continue

        elif letter == '[':
            continue

        elif letter == ']':
            row += 1
            col = 0
            continue

        elif letter == '\'':
            if board_string[i+1] == '\'':
                col += 1
                i+=1
                continue

        elif letter == ' ':
            continue

        if letter == '3' or letter == '2':
            board[row,col] = '' + letter + board_string[i+1]
            i+=1
        else:
            board[row,col] = letter

        col += 1

    return board

def update_board(input_word, board):
    board = np.array(board.split(','))

    word = np.array(input_word.split(','))
    if word.size % 3 > 0:
        return False

    index = 0

    while(index < word.size):
        letter = word[index]
        index += 1
        row = int(word[index])
        index += 1
        col = int(word[index])

        #If valid letter already exists in place, can't put new letter there so return false
        if board[row,col] in letters:
            return False

        board[row,col] = letter

    return board

#Find the whole word (horizontal) at the specified indices
def find_word_in_row(input_word, board, input_row, input_col):
    #check for continuation of word after input
    for col in range(input_col + 1, 15):
        letter = board[input_row,col]
        if not letter in letters:
            break

        row_word_indices = np.append(row_word_indices, [letter, input_row, col])

    #check for continuation of word before input
    for col in reverse(range(0, input_col - 1)):
        letter = board[input_row,col]
        if not letter in letters:
            break

        row_word_indices = np.append(row_word_indices, [letter, input_row, col])

        #sort based on column of letter and return
        return row_word_indices[row_word_indices[:,2].astype(np.int).argsort()]

#Find the whole word (vertical) at the specified indices
def find_word_in_col(input_word, board, input_row, input_col):
    #check for continuation of word after input
    for row in range(input_row + 1, 15):
        letter = board[row,input_col]
        if not letter in letters:
            break

        col_word_indices = np.append(col_word_indices, [letter, row, input_col])

    #check for continuation of word before input
    for row in reverse(range(0, input_row - 1)):
        letter = board[row,input_col]
        if not letter in letters:
            break

        col_word_indices = np.append(col_word_indices, [letter, row, input_col])

        #sort based on row of letter and return
        return col_word_indices[col_word_indices[:,1].astype(np.int).argsort()]


#Calculate the score for a move (note: does not check if each word is a scrabble word, also expects the input to be validated beforehand by Django)
#also probably expects word to come pre-sorted
def calculate(input_word, board):
    points = 0
    word_orientation = False
    word_score = 0
    triple_letters = np.array([])
    double_letters = np.array([])
    triple_words = np.array([])
    double_words = np.array([])

    input_word = np.array(input_word)

    connected_words = np.array([])

    #loop through input word. Mark multipliers and find connected words
    for letter_with_index in input_word:
        letter = letter_with_index[0]
        row = letter_with_index[1]
        col = letter_with_index[2]

        index_pair = [row,col]

        #mark multipliers for each letter in input word
        if index_pair in TRIPLE_LETTER_SCORE:
            triple_letters = np.append(triple_letters, index_pair)
        elif index_pair in DOUBLE_LETTER_SCORE:
            double_letters = np.append(double_letters,index_pair)
        elif index_pair in DOUBLE_WORD_SCORE:
            double_words = np.append(double_words, index_pair)
        elif index_pair in TRIPLE_WORD_SCORE:
            triple_words = np.append(triple_words, index_pair)

        #find connected word along axis
        if word_orientation == 'horizontal':
            connected_word = find_word_in_col(input_word, board, row,col)
        else:
            connected_word = find_word_in_row(input_word, board, row,col)

        #add connected word to list
        if len(connected_word) > 1:
            connected_words = np.append(connected_words, connected_word)



    # if input has multiple rows, its probably a vertical word
    if len(np.unique(input_word[:,1])) > 1:
        word_orientation = 'vertical'

    # if input has multiple cols, its probably a horizontal word, but if multiple cols and rows, its invalid so return False
    if len(np.unique(input_word[:,2])) > 1:
        if word_orientation == 'vertical':
            word_orientation = 'invalid'
            return False #might need to do something to send response later
        else:
            word_orientation = 'horizontal'

    row = input_word[0,1]
    col = input_word[0,2]

    if word_orientation == 'horizontal':
        word = find_word_in_row(input_word, board, row, col)
    else:
        word = find_word_in_col(input_word, board, row, col)
    if len(word) <= 1: #if word length is 1, then wrong direction was chosen
        word_orientation = 'horizontal'
        word = find_word_in_row(input_word, board, row, col)


    #add up sum of points for all letters in main word
    for letter_with_index in word:

        letter = letter_with_index[0]
        row = letter_with_index[1]
        col = letter_with_index[2]
        index_pair = [row,col]

        letter_score = int(points_map[letter])

        if index_pair in triple_letters:
            letter_score *= 3
        elif index_pair in double_letters:
            letter_score *= 2

        word_points += letter_score


    #Multiply word modifiers to main word score
    word_points *= 2**len(double_words) * 3**len(triple_words)

    #Calculate score for connected words
    for conn_word in connected_words:
        triple_multiplier = 1
        double_multiplier = 1
        connected_word_points = 0

        #calculate score for individual word
        for val in conn_word:
            letter = val[0]
            row = val[1]
            col = val[2]

            index_pair = [row,col]

            letter_score = int(points_map[letter])

            if index_pair in triple_letters:
                letter_score *= 3
            elif index_pair in double_letters:
                letter_score *= 2


            if index_pair in triple_words:
                triple_multiplier *= 3
            elif index_pair in double_words:
                double_multiplier *= 2

            connected_word_points += letter_score

        #apply multipliers to each word
        connected_word_points *= triple_multiplier * double_multiplier

        #add up points for move
        word_points += connected_word-points

    return word_points, word, connected_words



