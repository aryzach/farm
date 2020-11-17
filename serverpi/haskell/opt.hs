import Data.List
import Control.Monad
import System.Environment 

allMatrices :: Int -> Int -> [[[Int]]]
allMatrices timeSegments rows = replicateM timeSegments $ replicateM rows [0,1] 

criteriaFilter :: Int -> [Int] -> [[[Int]]] -> [[[Int]]] 
criteriaFilter minOn timeTotals ms = shortestTotalTimeFilter $ filter (\x -> timeSumsFilter timeTotals x && minimumOnFilter minOn x) ms 

timeSumsFilter :: [Int] -> [[Int]] -> Bool 
timeSumsFilter timeTotals (x:xs) = timeTotals == foldl (zipWith (+)) (replicate (length x) 0) (x:xs)

minimumOnFilter :: Int -> [[Int]] -> Bool
minimumOnFilter min xs = all (\y -> y >= min || y == 0) (map sum xs) 

shortestTotalTimeFilter :: [[[Int]]] -> [[[Int]]]
shortestTotalTimeFilter ms = 
        let     rz = map (filter (\m -> sum m /= 0)) ms
                shortestTime = minimum (map length rz)  
        in
                filter (\x -> length x == shortestTime) rz
  
optimalValveRuntimes :: Int -> [Int] -> [[[Int]]]
optimalValveRuntimes minOn timeTotals =  criteriaFilter minOn timeTotals $ allMatrices (sum timeTotals) (length timeTotals) 

optimal :: Int -> [Int] -> Maybe [[Int]]
optimal minOn timeTotals = safeHead $ optimalValveRuntimes minOn timeTotals

safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

main :: IO ()
main = do
        args <- getArgs
        let     minOn = args !! 0
                timeTotals = args !! 1
        print(optimal (read minOn :: Int) (map (\x -> read [x] :: Int) timeTotals))
