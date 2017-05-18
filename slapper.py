from PIL        import Image
from subprocess import run, PIPE
from os         import listdir
from os.path    import isfile, join

# Configuration

def mtgImagePathLookupScript():
    return "mtgchill"

def slapback():
    return Image.open("./SlapBack-200DPI.jpg")

def deckDir():
    return "Decks"

def outDir():
    return "Images"

# Logic

def mySplit(x):
  y = x.split()
  if len(y) < 2:
    return ["Sideboard", ""]
  return y

def getDecks():
    return [join(deckDir(), f) for f in listdir(deckDir()) if isfile(join(deckDir(), f))]

def getDecklists():
    result = {}
    for d in getDecks():
        result[d] = [(mySplit(line.strip())[0], (" ".join(mySplit(line.strip())[1:]))) for line in open(d)]
    return result

def mtgimg(x):
    imgPath = run([mtgImagePathLookupScript(), x], stdout=PIPE).stdout.decode('utf-8').strip()
    return Image.open(imgPath)

def render(d, n, x):
    renderPath = join(outDir(), d)
    filename = "".join([c for c in x if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    i0 = slapback()
    i1 = mtgimg(x)
    (i0x, i0y) = i0.size
    (i1x, i1y) = i1.size
    i2 = i1.crop((10, 10, i1x - 10, i1y - 10))
    (i2x, i2y) = i2.size
    ((pasteX, _x), (pasteY, _y)) = (divmod(i0x - i2x, 2), divmod(i0y - i2y, 2))
    i0.paste(i2, (pasteX, pasteY))
    run(["mkdir", "-p", renderPath])
    i0.save(join(renderPath, n + " " + filename + ".jpg"))

def debugMain():
    main()
    #print(mtgimg("Anger of the Gods"))

def main():
    ds = getDecklists()
    n  = 0
    for d in ds:
        d1 = d
        for c in ds[d]:
            if c[0] != "Sideboard" and c[0] != "":
                n = n + 1
                print((n, c[1]))
                render(d1, c[0], c[1])
            else:
                d1 = join(d1, "Sideboard")

if __name__ == "__main__":
    debugMain()
