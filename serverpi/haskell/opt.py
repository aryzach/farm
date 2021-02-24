import itertools

#allMatrices :: Int -> Int -> [[[Int]]]
#allMatrices timeSegments rows = replicateM timeSegments $ replicateM rows [0,1] 

def allMatricies(timeSegments, rows):
    rowM = [p for p in itertools.product([0,1], repeat=rows)]
    z = itertools.product(rowM, repeat=timeSegments)
    final = [g for g in z]
    return final 

def master(timeSegments, minOn):
    validStates = list(filter(lambda x: sum(x) >= minOn, [p for p in itertools.product([0,1], repeat=len(timeSegments))]))
    for state in validStates:
        if timeSumsCheck(timeSegments, [state]):
            return [state]
    for i in range(2,sum(timeSegments)):
        leastTimesPotential = [p for p in itertools.product(validStates, repeat=i)]
        # so this now has already been built so at least the min valves is on and is producing potential solutions with least time first 
        for potential in leastTimesPotential:
            if timeSumsCheck(timeSegments, potential):
                return potential 
    return []



#criteriaFilter :: Int -> [Int] -> [[[Int]]] -> [[[Int]]] 
#criteriaFilter minOn timeTotals ms = shortestTotalTimeFilter $ filter (\x -> timeSumsFilter timeTotals x && minimumOnFilter minOn x) ms 

def criteriaFilter(minOn, timeTotals, ms):
    return shortestTotalTimeFilter(filter(lambda x: timeSumsFilter(timeTotals, x) and minimumOnFilter(minOn,x), ms))

#timeSumsFilter :: [Int] -> [[Int]] -> Bool 
#timeSumsFilter timeTotals (x:xs) = timeTotals == foldl (zipWith (+)) (replicate (length x) 0) (x:xs)

def timeSumsFilter(timeTotals, lists):
    final = list(map(lambda x : x*0, list(range(0,len(lists[0])))))
    for l in lists:
        for i in range(0, len(l)):
            final[i] += l[i] 
    return timeTotals == final

def timeSumsCheck(timeTotals, potential):
    final = list(map(lambda x : x*0, list(range(0,len(potential[0])))))
    for l in potential:
        for i in range(0, len(final)):
            final[i] += l[i] 
    return timeTotals == final


#minimumOnFilter :: Int -> [[Int]] -> Bool
#minimumOnFilter min xs = all (\y -> y >= min || y == 0) (map sum xs) 

def minimumOnFilter(minNum,lists):
    sums = list(map(lambda x: sum(x), lists))
    for s in sums:
        if (s >= minNum) or s == 0:
            pass
        else:
            return False
    return True

#shortestTotalTimeFilter :: [[[Int]]] -> [[[Int]]]
#shortestTotalTimeFilter ms = 
#        let     rz = map (filter (\m -> sum m /= 0)) ms
#                shortestTime = minimum (map length rz)  
#        in
#                filter (\x -> length x == shortestTime) rz

def shortestTotalTimeFilter(ms):
    rz = list(map(lambda x: list(filter(lambda m: sum(m) != 0, x)), ms))
    times = map(lambda x: len(x), rz)
    shortestTime = min(times)
    return list(filter(lambda x: len(x) == shortestTime, rz))
  
#optimalValveRuntimes :: Int -> [Int] -> [[[Int]]]
#optimalValveRuntimes minOn timeTotals =  criteriaFilter minOn timeTotals $ allMatrices (sum timeTotals) (length timeTotals) 

def optimalValveRuntimes(minOn, timeTotals):
    return criteriaFilter(minOn,timeTotals, allMatricies(sum(timeTotals), len(timeTotals)))

#optimal :: Int -> [Int] -> Maybe [[Int]]
#optimal minOn timeTotals = safeHead $ optimalValveRuntimes minOn timeTotals
    
def optimal(minOn, timeTotals):
    try:
        return optimalValveRuntimes(minOn, timeTotals)
    except:
        print("bad")

#safeHead :: [a] -> Maybe a
#safeHead [] = Nothing
#safeHead (x:_) = Just x

#main :: IO ()
#main = do
#        args <- getArgs
#        let     minOn = args !! 0
#                timeTotals = args !! 1
#        print(optimal (read minOn :: Int) (map (\x -> read [x] :: Int) timeTotals))


