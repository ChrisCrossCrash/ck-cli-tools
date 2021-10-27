import os

if __name__ == '__main__':
    folders = os.environ['PATH'].split(';')
    for folder in folders:
        if folder:
            print(folder)
