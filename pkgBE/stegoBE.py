import numpy as np
from PIL import Image

"""This iteration of the stego script is going to be imported by my django project and
we will use this iteration of the script as a module to pass user input to and return an encoded
or decoded image/message
Currently import requires sys.path.append to find project and then from stegoBE import encode, decode, or *
"""

"""First we need to create a function that is callable externally and use that instead of doing
all this work in the view. We will save our files to /media/uploads/{uploaded_file_name}
Upload file name is an amalgamation of hashes which are then used as primary key. This is preferred
over using the ID as the pk as then all other "secret" messages are shown to anyone who can pollute
URL and since this is django that isn't hard. At least this way you need to already know the information
in order to "guess" the URL
"""

"""Hashing is working for generating file names based on hash of both image and message to prevent collisions hopefully
, but this had the unintended effect of not having unique primary keys and getting errors when using as primary which is
really only a visible problem when decoding, but to prevent that we can just check if the obj already exists and return
that
"""

"""Need to adjust this function. I am limiting amount of text stored to 200 chars and need to investigate
optimizing this code. Also should convert whichever image to png before I do anything to prevent other problems maybe"""
def encode(src, message, dest):

    # first we open the image
    img = Image.open(src, 'r')

    img_seq = img.getdata()

    # set vars for width and height of image
    width, height = img.size

    # create numpy array of pixel values
    image_array = np.array(img_seq, dtype=np.uint8)

    file_extension = '.png'

    # check mode to see how many columns we will have for each pixel value
    if img.mode == 'RGB':
        columns = 3
    elif img.mode == 'RGBA':
        columns = 4

    # need a tag for knowing when to stop
    end_pattern = ' stegomyego'
    to_encode = message + end_pattern
    dest += file_extension
    # convert message into 8 bit values (convert char to ord ord to bitstring)
    b_message = ''.join([format(ord(i), "08b") for i in to_encode])

    idx = 0
    """TODO: Need to come up with a way to fail and return that to the view"""
    # nested for loop to access each pixels RGB//RGBA value convert to binary (these are
    # stored as 0x10010101 at first so lop off the 0x and grab everything except the LSB which will come
    # from the message. needs the ,2 because of the call to bin I believe
    for row in range(len(image_array)):
        for col in range(0, columns):
            value = image_array[row][col]
            binary_value = f'{value:08b}'
            if idx < len(b_message):
                temp_string = binary_value[:-1]
                new_string = temp_string + b_message[idx]
                new_value = int(new_string, 2)
                image_array[row][col] = new_value
                idx += 1
            elif idx > len(b_message):
                image_array[row][col] = image_array[row][col]
                idx += 1

    image_array = np.reshape(image_array, (height, width, columns))
    enc_img = Image.fromarray(image_array)
    enc_img.save(dest)

"""This decode function will also be imported and used for decoding and returning to view"""


def decode(src):
    # open the image in read
    img = Image.open(src, 'r')

    # create the array of pixel values
    decode_seq = img.getdata()
    decode_array = np.array(decode_seq, dtype=np.uint8)

    # We need to know the mode for our loop
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    # init empty string to hold hidden bizzits
    hidden_bits = ""
    # the return of the nested for loop, not seeing where N is involved might refactor
    for p in range(len(decode_array)):
        for q in range(0, n):
            value = decode_array[p][q]
            binary_value = f'{value:08b}'
            last_bit = binary_value[-1]
            hidden_bits += last_bit

    chunks = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    endpattern = "stegomyego"

    # Compute the hidden message for the hidden bits and end when the end says stego
    message = ""
    for chunk in chunks:
        if message[-10:] == endpattern:
            pass
        else:
            x = chr(int(chunk, 2))
            message += x

    return str(message)
