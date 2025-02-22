# --------------------------------------------------------------------------------------------------------
#                                         IMPORTING LIBRARIES 

import os
from AppKit import NSPasteboard, NSStringPboardType

# --------------------------------------------------------------------------------------------------------

def copy_clipboard():
    # Check if the file exists, create if it doesn't
    file_exists = os.path.exists("clipboard.txt")
    
    with open("clipboard.txt", "a") as f:
        if not file_exists:
            f.write("Clipboard log initiated.\n")
        
        try:
            # Access clipboard content
            pasteboard = NSPasteboard.generalPasteboard()
            content = pasteboard.stringForType_(NSStringPboardType)
            
            if content:
                f.write("\n\nClipBoard Data:\n" + content)
            else:
                f.write("\n\nClipboard is empty or not text.")
        except Exception as e:
            f.write("\n\nCouldn't copy clipboard data: " + str(e))

# copy_clipboard()   