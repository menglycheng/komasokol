import qrcode
import os

def generate_qrcode(chat_id,username):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"{chat_id}-{username}"
    qr.add_data(data)
    qr.make(fit=True)
    

    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{chat_id}.png"
    img.save(filename)
    return "done"

def register_patient(chat_id,username):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"{username}"
    qr.add_data(data)
    qr.make(fit=True)
    

    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{chat_id}.png"
    img.save(filename)
    return "done"

# function to delete the qrcode
def delete_qrcode(chat_id):
    filename = f"{chat_id}.png"
    if os.path.exists(filename):
        os.remove(filename)
        return "done"
    else:
        return "The file does not exist"
