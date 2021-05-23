say a
#set func s3_tp:load
    #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
        #mc setblock ~ ~ ~ <treetype>_log
    #set tag block #s3_tp:air
        execute if block ~ ~ ~ air
        execute if block ~ ~ ~ #acacia_logs
    #set tag entity #s3_tp:some
        execute if entity @e[type=pig]
        execute if entity @e[type=enderman]
    #set tag func #s3_tp:test
        function #load
        function #s3_tp:awa
    #set tag fluid #s3_tp:awawa
        #water
        # lava
execute if block ~ ~ ~ #acacia_logs
