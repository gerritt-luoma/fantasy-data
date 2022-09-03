import os, sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
load_dotenv('../.env')

from main import main

if __name__ == '__main__':
    main()