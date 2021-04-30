
lisMain=[1,]

def A(x, main):
    sub = [1,]
    if x <= 0:
        return 
    else:
        x = x - 1
        sub.append(x)
        main.append(x)
        A(x, main)
    print("x: ",  x)
    print(sub)
A(3, lisMain)

print(lisMain)