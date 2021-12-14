type Depth = Int
type Horizontal = Int
type Position = (Depth, Horizontal)
type Command  = (String, Int)

parseInput :: String -> [Command]
parseInput s = zip (map head coms) (map (read . last) coms)
  where coms = map words $ lines s

-- | Given a starting position and a command,
--   return the position after executing the command
commandOne :: Position -> Command -> Position
commandOne (x, y) (direction, d) =
  case direction of
    "down"    -> (x + d, y)
    "up"      -> (x - d, y)
    "forward" -> (x, y + d)
    _         -> error "Invalid command"

taskOne :: [Command] -> Int
taskOne coms = x * y 
  where (x, y) = foldl commandOne (0, 0) coms

commandTwo :: (Position, Int) -> Command -> (Position, Int)
commandTwo ((x, y), aim) (direction, d) =
  case direction of 
    "down"    -> ((x, y), aim + d)
    "up"      -> ((x, y), aim - d)
    "forward" -> ((x + (d * aim), y + d), aim)
    _         -> error "Invalid command"

taskTwo :: [Command] -> Int
taskTwo coms = x * y
  where (x, y) = fst $ foldl commandTwo ((0, 0), 0) coms

main = do
  input <- getContents
  let commands = parseInput input
  print $ taskOne commands
  print $ taskTwo commands