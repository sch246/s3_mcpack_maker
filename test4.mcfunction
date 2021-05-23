say a
#set func s3_tp:load
    #let list1 = ['oak','birch','spruce','dark_oak','acacia']
    #run dic['list1'].append('jungle')
    #let list2 = []
    #for_ <num> in range(0,len(dic['list1']))
        #let list2 = dic['list2'] + [(dic['list1'][<num>],<num>+1,2*<num>+1)]
        #let tree = dic['list1'][<num>] + '_log'
        #let i = <num>+1
        #let j = <num>*2+1
        ##print_ (dic['i'],dic['j'],dic['tree'])
        #mc setblock ~ ~dic['i'] ~dic['j'] dic['tree']
    #print_ dic['list1']
    #print_ dic['list2']
    #az
