import Data.Char (digitToInt)
import Data.List (foldl', maximumBy, group, sort, transpose, minimumBy)
import Data.Ord (comparing)

binToDec :: String -> Int
binToDec = foldl' (\acc x -> acc * 2 + digitToInt x) 0

mostCommon :: (Eq a, Ord a) => [a] -> a
mostCommon = head . maximumBy (comparing length) . group . sort

leastCommon :: (Eq a, Ord a) => [a] -> a
leastCommon = head . minimumBy (comparing length) . group . sort

taskOne :: [String] -> Int
taskOne s = binToDec (map mostCommon $ transpose s) * binToDec (map leastCommon $ transpose s)

main = do
  input <- getContents
  let numbers = lines input
  print $ taskOne numbers