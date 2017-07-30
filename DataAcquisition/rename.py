import os

# Use a raw string, to reduce errors with \ characters.
folder = r"D:\Friends"

old = '%20'
new = ' '

for root, dirs, filenames in os.walk(folder):
 for filename in filenames:
    if old in filename: # If a '+' in the filename
      filename = os.path.join(root, filename) # Get the absolute path to the file.
      print (filename)
      os.rename(filename, filename.replace(old,new)) # Rename the file