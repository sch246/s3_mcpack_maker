#set func s3_tp:load
    #let list1 = ['oak','birch','spruce','dark_oak','acacia','jungle']
    #for_ num in range(0,len(<list1>))
        #mc setblock ~ ~f{<num>+1} ~f{<num>*2+1} f{<list1>[<num>] + '_log'}
