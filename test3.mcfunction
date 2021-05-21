say a
#set func s3_tp:load
    #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
        #let az = 'treetype'
        #let az = dic['az']+'_log'
        #if_ dic['az'] == 'oak_log'
            #mc setblock ~ ~100 ~ treetype_log
        #else_
            #mc setblock ~ ~ ~ treetype_log
execute if block ~ ~ ~ #acacia_logs
