from PIL import Image
from mapper import Wad

if __name__ == "__main__":
    wad = Wad("./Doom1.WAD")

    level_1 = wad.levels[0]
    level_1.save_svg()
    print str(level_1.name)+".svg"
    im = Image.open(str(level_1.name)+".svg")
    im.show()
