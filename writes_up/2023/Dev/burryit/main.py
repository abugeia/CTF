import gzip as gz
import lzma as xz
import filetype

def main():
    with open('buryit', 'rb') as f:
        data = f.read()
        kind = filetype.guess(data)
        while(kind != None):
            if kind.extension == 'gz':
                data = gz.decompress(data)
            else:
                data = xz.decompress(data)
            kind = filetype.guess(data)
        print(data.decode())

if __name__ == '__main__':
    main()