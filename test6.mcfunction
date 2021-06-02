    
#dic load json range to range
#dic set range.predicate.position.x.min value 0
#dic remove range.condition
#dic save predicate s3.raycast:b from range
# 等价于
#dic load json range to range
#let range.predicate.position.x.min = 0
#run removenbt('range.condition',dic)
#dic save predicate s3.raycast:b from range

