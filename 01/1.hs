main = do
  input <- getContents
  let xs = map read (words input)
  print $ depthOne xs
  print $ depthTwo xs

depthOne :: [Int] -> Int
depthOne xs = length $
  filter (== True) $
  zipWith (<) xs (tail xs)

windowed :: Int -> [a] -> [[a]]
windowed n xs
    | length xs < n = []
    | otherwise     = take n xs : windowed n (tail xs)

depthTwo :: [Int] -> Int
depthTwo xs = length $
  filter (== True) $
  zipWith (\ys zs -> sum ys < sum zs) wndwd (tail wndwd)
        where wndwd = windowed 3 xs
