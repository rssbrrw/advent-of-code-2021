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
taskOne ss = binToDec (map mostCommon $ transpose ss) * binToDec (map leastCommon $ transpose ss)

oxygen :: [String] -> Int
oxygen ss = binToDec $ head $ foldl filterMostCommonAtIndex ss [0..length (head ss) - 1]

co2 :: [String] -> Int
co2 ss = binToDec $ head $ foldl filterLeastCommonAtIndex ss [0..length (head ss) - 1]

taskTwo :: [String] -> Int
taskTwo ss = oxygen ss * co2 ss

-- | For a matrix and index i, return only the rows from the matrix
--   whose element at i is the most common at that index
filterMostCommonAtIndex :: [String] -> Int -> [String]
filterMostCommonAtIndex ss i = filterForIndex ss i mostCommon

-- | For a matrix and index i, return only the rows from the matrix
--   whose element at i is the least common at that index
filterLeastCommonAtIndex :: [String] -> Int -> [String]
filterLeastCommonAtIndex ss i = filterForIndex ss i leastCommon

filterForIndex :: [String] -> Int -> (String -> Char) -> [String]
filterForIndex ss i func = filter (\w -> (w !! i) == func (transpose ss !! i)) ss

main = do
  input <- getContents
  let numbers = lines input
  print $ taskOne numbers
  print $ taskTwo numbers
