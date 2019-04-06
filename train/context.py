import os
def get_classes(directory):
    words=[]
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
                path=os.path.join(root,file)
                word=os.path.basename(os.path.dirname(path))
                if not word in words:
                    words.append(word)
    return words,len(words)

