say a
#set func s3_tp:load
    #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
        #mc setblock ~ ~ ~ <treetype>_log
    #addtag block #s3_tp:air
        execute if block ~ ~ ~ air
        execute if block ~ ~ ~ #acacia_logs
    #addtag entity #s3_tp:some
        execute if entity @e[type=pig]
        execute if entity @e[type=enderman]
    #addtag func #s3_tp:test
        function #load
        function #s3_tp:awa
    #addtag fluid #s3_tp:awawa
        #water
        # lava
execute if block ~ ~ ~ #acacia_logs
