#set func s3_tp:load
    #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
        #let az = <treetype>
        #let az = <az>+'_log'
        #if_ <az> == 'oak_log'
            #mc setblock ~ ~100 ~ <treetype>_log
        #else_
            #mc setblock ~ ~ ~ <treetype>_log
