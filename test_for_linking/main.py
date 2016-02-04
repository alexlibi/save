import add, sub, mult_div, getopt, sys

if __name__ == '__main__':
    
    try:
        arg, opt = getopt.getopt(sys.argv[1:],"a:")
    except getopt.GetoptError as err:
        sys.exit(2)
    
    a, b=float(opt[0]), float(opt[1])
        
    print(add.add(a,b))
    print(sub.sub(a,b))
    print(mult_div.div(a, b))
    print(mult_div.div(a, b))