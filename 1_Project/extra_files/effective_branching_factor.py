def branching_factor(N, b, d, tolerance):

    aux_value = 0
    for i in range(1, d+1):
        aux_value += b**i

    if N < aux_value + tolerance and N > aux_value-tolerance:

        return True

    else:
        
        return False

def frange(x, y, step):
    while x < y:
        yield x
        x += step

def main():

    tol = 1

    for b in frange(0.1, 50, 0.001):

        result  = branching_factor(27305+13807, b, 3, tol)

        if result:
            print("%.3f"% b)
            break

if __name__=="__main__":
    main()
    

