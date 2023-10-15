import os
# Loop through all files in the directory and its subdirectories
for root, dirs, files in os.walk("./"):
    # Filter out hidden folders (those starting with a dot)
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for file in files:
        file_path = os.path.join(root, file)

        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            try :
                  with open(file_path, 'r') as f:
     
                    file_contents = f.read()
                    print(file)
                
            except:
                pass
            # You can read the contents of the file here
          
          
          
          
                # Do something with the file contents

        # If you want to process non-text files, you might use a different approach
        # For example, to process binary files, you might use a library like 'binaryfile'

        # You can also use other libraries like 'Pandas' for structured data
        # For example, to read CSV files, you can use 'pandas.read_csv(file_path)'

# This code will recursively traverse the directory, ignoring hidden folders, and read all files
