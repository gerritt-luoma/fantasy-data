import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from main import main

print(sys.path)
if __name__ == '__main__':
    main()