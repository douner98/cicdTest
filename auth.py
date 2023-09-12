def login(_id):
    result = False;
    members = ['egoing', 'k8805', 'leezche']
    x = 0;
    for member in members:
        
        print("count" , x)
        if member == _id:
            result = True
            break
        
        x = x + 1;

    return result