def check_rules(aij, ajk):
    aik = None
    
    # Rule 1
    if (aij == "≈" and ajk == "≈"):
        aik = {"≈","⊏", "⊐"}
    
    # Rule 2a
    if (aij == "≈" and ajk == "⊏") or (aij == "⊏" and ajk == "≈"):
        aik = {"≈", "⊏" , "⊂"}
    
    # Rule 2b
    if (aij == "≈" and ajk == "⊂") or (aij == "⊂" and ajk == "≈"):
        aik = {"⊏", "⊂", "<"}
    
    # Rule 2c
    if (aij == "≈" and ajk == "<") or (aij == "<" and ajk == "≈"):
        aik = {"⊂", "<", "≺"}
    
    # Rule 3
    if (aij == "≈" and ajk == "≺") or (aij == "≺" and ajk == "≈"):
        aik = {"<" , "≺"}
    
    # Rule 4a
    if (aij == "⊏" and ajk == "⊏"):
        aik = {"⊏", "⊂", "<"}
    
    # Rule 4b
    if (aij == "⊂" and ajk == "⊏") or (aij == "⊏" and ajk == "⊂"):
        aik = {"⊂", "<", "≺"}
    
    # Rule 4c
    if (aij == "<" and ajk == "⊏") or (aij == "⊏" and ajk == "<"):
        aik = {"<" , "≺"}
    
    # Rule 5a
    if (aij == "⊏" and ajk == "≺") or (aij == "≺" and ajk == "⊏"):
        aik = {"≺"}
        
    # Rule 5b
    if (aij == "⊂" and ajk == "≺") or (aij == "≺" and ajk == "⊂"):
        aik = {"≺"}
        
    # Rule 5c
    if (aij == "<" and ajk == "≺") or (aij == "≺" and ajk == "<"):
        aik = {"≺"}
    
    # Rule 5d
    if (aij == "≺" and ajk == "≺") or (aij == "≺" and ajk == "≺"):
        aik = {"≺"}
    
    # Rule 6a
    if (aij == "⊂" and ajk == "<") or (aij == "<" and ajk == "⊂"):
        aik = {"≺"}
        
    # Rule 6b
    if (aij == "<" and ajk == "<"):
        aik = {"≺"}
    
    # Rule 7
    if (aij == "⊂" and ajk == "⊂"):
        aik = {"<", "≺"}
    
    # Rule 8a
    if (aij == "≈" and ajk == "⊐") or (aij == "⊐" and ajk == "≈"):
        aik = {"≈" , "⊐" , "⊃"}
        
    # Rule 8b
    if (aij == "≈" and ajk == "⊃") or (aij == "⊃" and ajk == "≈"):
        aik = {"⊐" , "⊃" , ">"}
        
    # Rule 8c
    if (aij == "≈" and ajk == ">") or (aij == ">" and ajk == "≈"):
        aik = {"⊃" , ">" , "≻"}
        
    # Rule 8d
    if (aij == "≈" and ajk == "≻") or (aij == "≻" and ajk == "≈"):
        aik = {">" , "≻"}
    
    # Rule 9a 
    if (aij == "⊐" and ajk == "⊐"):
        aik = {"⊐" , "⊃" , ">"}
    
    # Rule 9b 
    if (aij == "⊐" and ajk == "⊃") or (aij == "⊃" and ajk == "⊐"):
        aik =  {"⊃" , ">" , "≻"}
        
    # Rule 9c 
    if (aij == "⊐" and ajk == ">") or (aij == ">" and ajk == "⊐"):
        aik = {">" , "≻"}
        
    # Rule 9d 
    if (aij == "⊐" and ajk == "≻") or (aij == "≻" and ajk == "⊐"):
        aik = {"≻"}
    
    # Rule 10 a
    if (aij == "⊃" and ajk == "⊃") :
        aik = {">" , "≻"}
    
    # Rule 10 b
    if (aij == "⊃" and ajk == ">") or (aij == ">" and ajk == "⊃") :
        aik = {"≻"}
        
    # Rule 10 c
    if (aij == "⊃" and ajk == "≻") or (aij == "≻" and ajk == "⊃"):
        aik = {"≻"}
    
    # Rule 11 a
    if (aij == ">" and ajk == ">"):
        aik = {"≻"}
        
    # Rule 11 b
    if (aij == ">" and ajk == "≻") or (aij == "≻" and ajk == ">"):
        aik = {"≻"}
    
    # Rule 12
    if (aij == "≻" and ajk == "≻"):
        aik ={"≻"}
    
    # Rule 13 a
    if (aij == "⊐" and ajk == "⊏") or (aij == "⊏" and ajk == "⊐"):
        aik = {"≈" , "⊏" , "⊐"}
        
    # Rule 13 b
    if (aij == "⊐" and ajk == "⊂") or (aij == "⊂" and ajk == "⊐"):
        aik = {"≈" , "⊏" , "⊂"}
        
    # Rule 13 c
    if (aij == "⊐" and ajk == "<") or (aij == "<" and ajk == "⊐"):
        aik = {"⊏" , "⊂" , "<"}
        
    # Rule 13 d
    if (aij == "⊐" and ajk == "≺") or (aij == "≺" and ajk == "⊐"):
        aik = {"⊂" , "<" , "≺"}
    
    # Rule 14 a
    if (aij == "⊃" and ajk == "⊏") or (aij == "⊏" and ajk == "⊃"):
        aik = {"≈" , "⊐" , "⊃"}
        
    # Rule 14 b
    if (aij == "⊃" and ajk == "⊂") or (aij == "⊂" and ajk == "⊃"):
        aik = {"≈" , "⊏" , "⊐"}
        
    # Rule 14 c
    if (aij == "⊃" and ajk == "<") or (aij == "<" and ajk == "⊃"):
        aik = {"≈" , "⊏" , "⊂"}
        
    # Rule 14 d
    if (aij == "⊃" and ajk == "≺") or (aij == "≺" and ajk == "⊃"):
        aik =  {"⊏" , "⊂" , "<" , "≺"}
    
    # Rule 15 a
    if (aij == ">" and ajk == "⊏") or (aij == "⊏" and ajk == ">"):
        aik = {"⊐" , "⊃" , ">"}
    
    # Rule 15 b
    if (aij == ">" and ajk == "⊂") or (aij == "⊂" and ajk == ">"):
        aik = {"≈" , "⊐" , "⊃"}
        
    # Rule 15 c
    if (aij == ">" and ajk == "<") or (aij == "<" and ajk == ">"):
        aik = {"≈" , "⊏" , "⊐"}
        
    # Rule 15 d
    if (aij == ">" and ajk == "≺") or (aij == "≺" and ajk == ">"):
        aik = {"≈" , "⊏" , "⊂" , "<" , "≺"}
        
        
    # Rule 16 a
    if (aij == "≻" and ajk == "⊏") or (aij == "⊏" and ajk == "≻"):
        aik = {"⊃" , ">" , "≻"}
    
    # Rule 16 b    
    if (aij == "≻" and ajk == "⊂") or (aij == "⊂" and ajk == "≻"):
        aik = {"⊐" , "⊃" , ">" , "≻"}
    
    # Rule 16 c    
    if (aij == "≻" and ajk == "<") or (aij == "<" and ajk == "≻"):
        aik = {"≈" , "⊐" , "⊃" , ">" , "≻"}
    
    # Rule 16 d    
    if (aij == "≻" and ajk == "≺") or (aij == "≺" and ajk == "≻"):
        aik = {"≈" , "⊏" , "⊂" , "<" , "≺" , "⊐" , "⊃" , ">" , "≻"}
    
    return aik
