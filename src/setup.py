from distutils.core import setup
import py2exe

setup(windows=['main.py'],
      data_files=[("bilder",
                   ["..\images\auto.png",
                    "..\images\catEating.png",
                    "..\images\catRoaming.png",
                    "..\images\food.png",
                    "..\images\level1.png",
                    "..\images\nedde.png",
                    "..\images\scenery",
                    "..\images\testworld.PNG",
                    "..\images\testworld2.PNG"]
                   ),
                  ("sounds",
                   ["..\sounds\meow.ogg"]
                   ),
                  ],
      dist_dir="StreetCats")
