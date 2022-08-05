import hashlib
from PIL import Image


def hashbytessha256(message, img):
    message_hash = hashlib.sha256(message.encode())
    image_hash = hashlib.sha256(Image.open(img).tobytes())
    combo_hash = str(message_hash.hexdigest()) + str(image_hash.hexdigest())
    combo_hash_obj = hashlib.sha256(combo_hash.encode())
    combo_hash_fn = combo_hash_obj.hexdigest()
    hashDict = {"Message Hash": message_hash.hexdigest(),
                "Image Hash": image_hash.hexdigest(),
                "FileName Hash": combo_hash_fn}

    return hashDict


def hash2to1(email_addy, content):
    email_hash = hashlib.sha256(email_addy.encode())
    content_hash = hashlib.sha256(content.encode())
    content_address_string = str(email_hash.hexdigest()) + str(content_hash.hexdigest())
    content_address_ob = hashlib.sha256(content_address_string.encode())
    content_address_hash = content_address_ob.hexdigest()

    return content_address_hash