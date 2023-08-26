import sys
import getopt
  
def full_name():
    first_name = None
    last_name = None
  
    argv = sys.argv[1:]
  
    try:
        opts, args = getopt.getopt(argv, "f:m:l:", 
                                   ["first_name=",
                                    "middle_name=",
                                    "last_name="])
      
    except:
        print("Error")
  
    for opt, arg in opts:
        if opt in ['-f', '--first_name']:
            first_name = arg
        elif opt in ['-m', '--middle_name']:
            middle_name = arg
        elif opt in ['-l', '--last_name']:
            last_name = arg
      
  
    print(first_name+middle_name+last_name)
  
full_name()