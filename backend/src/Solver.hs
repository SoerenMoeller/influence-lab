import Types
  ( Statement(..)
  , Variable(..)
  , Interval(..)
  , Scheme(..)
  , Behaviour(..)
  , StatementList(..), mkInterval)

import qualified Scheme.IO as IO
import qualified Scheme.Points as Points

import Data.Map (Map, (!))
import qualified Data.Map as Map
import Control.Monad (forM_)
import Data.List (nub, null)
import qualified Data.Set as Set
import SAT.MiniSat

scheme :: Scheme
scheme = IO.statementListToScheme . IO.tuplesToStatements $
    [ ("a", (0, 1), ANTI, (0, 2), "b")
    , ("b", (0, 1), MONO, (0, 2), "d")
    , ("b", (1, 2), MONO, (0, 2), "d")
    , ("a", (0, 1), CONST, (0, 1), "d")
    , ("a", (0, 1), MONO, (0, 2), "c")
    , ("c", (0, 2), MONO, (0, 2), "d")
    ]

reachable :: Variable -> Scheme -> [Variable]
reachable v (Scheme m) = Map.keys . Map.findWithDefault Map.empty v $ m

post :: Variable -> Scheme -> [Variable]
post v (Scheme m) = filter intermediate . reachable v $ Scheme m
  where
    intermediate :: Variable -> Bool
    intermediate v' = not . any (\v'' -> v'' `elem` reachable v (Scheme m) && v' `elem` reachable v'' (Scheme m)) $ variables
postAll :: [Variable] -> Scheme -> [Variable]
postAll vs scheme = nub . concatMap (`post` scheme) $ vs

variables :: [Variable]
variables = [Variable "a", Variable "b", Variable "c", Variable "d"]

pre :: Variable -> Scheme -> [Variable]
pre v (Scheme m) = filter (\v' -> v `elem` post v' (Scheme m)) $ variables

isMaximal :: Variable -> Scheme -> Bool
isMaximal v scheme = null . (`postAll` scheme) . post v $ scheme

distTP :: Variable -> Double -> Double -> Scheme -> Integer
distTP v x y scheme = sum . map (distTP' x y scheme v) . post v $ scheme

distTP' :: Double -> Double -> Scheme -> Variable -> Variable -> Integer
distTP' x y (Scheme m) v1 v2
    | isMaximal v1 scheme = 0
    | otherwise = (+) 2 . sum . zipWith (\ i i' -> 2 + distTP v2 i i' (Scheme m)) bds . drop 1 $ bds
  where
    matchingStatement = head . filter ((==) (Interval x y) . domain)  $ (m ! v1) ! v2
    (l, u) = (start . range $ matchingStatement, end . range $ matchingStatement)
    bds = filter (\p -> p >= l && p <= u) . Points.boundaries v2 $ scheme

getSubScheme :: Variable -> Variable -> Scheme -> [Statement]
getSubScheme v1 v2 (Scheme m) = m ! v1 ! v2

isSubInterval :: Interval -> Interval -> Bool
isSubInterval (Interval x1 y1) (Interval x2 y2) = x1 >= x2 && y1 <= y2

domInverse :: Variable -> Variable -> Scheme -> Double -> Double -> [Interval]
domInverse v1 v2 scheme x y = map domain . filter (isSubInterval (mkInterval x y) . range) . getSubScheme v1 v2 $ scheme

distPoi :: Variable -> Double -> Double -> Scheme -> Integer
distPoi v x y scheme = sum . map (\v' -> distPoi' x y scheme v' v) . pre v $ scheme

distPoi' :: Double -> Double -> Scheme -> Variable -> Variable -> Integer
distPoi' x y scheme v1 v2 = sum . map ((+) 2 . distPoiRec) . domInverse v1 v2 scheme x $ y
  where
    distPoiRec :: Interval -> Integer
    distPoiRec (Interval x1 y1) = distPoi v1 x1 y1 scheme

dist :: Variable -> Double -> Double -> Scheme -> Integer
dist v x y scheme = distTP v x y scheme + distPoi v x y scheme

size :: Variable -> Scheme -> Integer
size v scheme = (+) 1 . sum . zipWith (\ x' y' -> dist v x' y' scheme) ps . drop 1 $ ps
  where
    ps = Points.boundaries v scheme

getOriginalPoint :: Variable -> Double -> Scheme -> Integer
getOriginalPoint v x scheme = sum . zipWith (\ x' y' -> 1 + dist v x' y' scheme) ps . drop 1 $ ps
  where
    ps = takeWhile (<= x) . Points.boundaries v $ scheme

data SatVar = SatVar
  { variableFrom :: Variable
  , variableTo :: Variable
  , ptDom :: Integer
  , ptRng :: Integer
  } deriving (Eq, Show, Ord)

phiMax1 :: Scheme -> Formula SatVar
phiMax1 (Scheme m) = All
    [ Not (Var (SatVar a b i j)) :||: Not (Var (SatVar a b i j'))
    | a <- variables
    , b <- variables
    , b `elem` reachable a (Scheme m)
    , i <- [0..size a (Scheme m)]
    , j <- [0..size b (Scheme m)]
    , j' <- [0..size b (Scheme m)]
    , j < j'
    ]

phiSome :: Scheme -> Variable -> Variable -> Integer -> Formula SatVar
phiSome (Scheme m) a b j = Some
    [ Var (SatVar a b j j')
    | j' <- [0..size b (Scheme m)]
    ]

phiGap :: Scheme -> Formula SatVar
phiGap (Scheme m) = All
    [(Var (SatVar a b i i') :&&: Var (SatVar a b k k'))
       :->: phiSome (Scheme m) a b j |
       a <- variables,
       b <- variables,
       b `elem` reachable a (Scheme m),
       i <- [0 .. size a (Scheme m)],
       j <- [0 .. size a (Scheme m)],
       i < j,
       k <- [0 .. size a (Scheme m)],
       j < k,
       i' <- [0 .. size b (Scheme m)],
       k' <- [0 .. size b (Scheme m)]]

phiComp :: Scheme -> Formula SatVar 
phiComp (Scheme m) = All 
    [ (Var (SatVar a b i j) :&&: Var (SatVar b c j k)) :->: Var (SatVar a c i k)
    | a <- variables
    , b <- variables
    , b `elem` reachable a (Scheme m)
    , c <- variables
    , c `elem` reachable b (Scheme m)
    , i <- [0..size a (Scheme m)] 
    , j <- [0..size b (Scheme m)] 
    , k <- [0..size c (Scheme m)] 
    ]

phiSts :: Scheme -> Formula SatVar 
phiSts (Scheme m) = All 
    [ phiStsRng (Scheme m) a b st :&&: phiStsBeh (Scheme m) a b st
    | a <- variables
    , b <- variables
    , b `elem` reachable a (Scheme m)
    , st <- getSubScheme a b (Scheme m)
    ]

phiStsRng :: Scheme -> Variable -> Variable -> Statement -> Formula SatVar
phiStsRng (Scheme m) a b st = All 
    [ Some 
        [ Var (SatVar a b i' j)
        | j <- [0..size b (Scheme m)]
        , getOriginalPoint b l (Scheme m) <= j
        , j <= getOriginalPoint b u (Scheme m)

        ]
    | i' <- [0..size a (Scheme m)]
    , getOriginalPoint a i (Scheme m) <= i' 
    , i' <= getOriginalPoint a is (Scheme m)
    ]
  where
    (i, is) = (start . domain $ st, end . domain $ st)
    (l, u)  = (start . range $ st, end . range $ st)

phiStsBeh :: Scheme -> Variable -> Variable -> Statement -> Formula SatVar
phiStsBeh (Scheme m) a b st = All 
    [ Var (SatVar a b i' j) :->: Some
        [ Var (SatVar a b i' j)
        | j' <- [0..size b (Scheme m)] 
        , behaviour st /= MONO  || j' >= j
        , behaviour st /= ANTI  || j' <= j
        , behaviour st /= CONST || j' == j
        ]
    | i'  <- [0..size a (Scheme m)]
    , getOriginalPoint a i (Scheme m) <= i' 
    , i'' <- [0..size a (Scheme m)]
    , i' < i''
    , i'' <= getOriginalPoint a is (Scheme m)
    , j <- [0.. size b (Scheme m)]
    ]
  where
    (i, is) = (start . domain $ st, end . domain $ st)

phi :: Scheme -> Formula SatVar 
phi scheme = All $ map ($ scheme) [phiMax1, phiGap, phiComp, phiSts]

-- data ExperimentPoints = ExperimentPoints
--   { variableFrom :: Variable
--   , variableTo :: Variable 
--   , x :: Double 
--   , y :: Double
--   }

solvePhi :: Formula SatVar -> [SatVar]
solvePhi formula = case solve formula of 
    Nothing     -> error "Not satisfiable"
    Just result -> map fst . filter snd . Map.toList $ result


main :: IO ()
main = do 
    forM_ ["d", "c", "b", "a"] $ \v -> do
        let ps = Points.boundaries (Variable v) scheme
        forM_ (zip ps (drop 1 ps)) $ \(p1, p2) -> do
            let dist = distTP (Variable v) p1 p2 scheme
            putStrLn $ "distTP(" ++ v ++ ", " ++ show p1 ++ ", " ++ show p2 ++ ") = " ++ show dist
    putStrLn "---------------------"
    forM_ ["d", "c", "b", "a"] $ \v1 -> do
        forM_ (post (Variable v1) scheme) $ \v2 -> do
            let ps = Points.boundaries (Variable v1) scheme
            forM_ (zip ps (drop 1 ps)) $ \(p1, p2) -> do
                let dist = distTP' p1 p2 scheme (Variable v1) v2
                putStrLn $ "distTP'(" ++ v1 ++ ", " ++ show v2 ++ ", " ++ show p1 ++ ", " ++ show p2 ++ ") = " ++ show dist
    putStrLn "====================="
    forM_ ["a", "b", "c", "d"] $ \v -> do
        let ps = Points.boundaries (Variable v) scheme
        forM_ (zip ps (drop 1 ps)) $ \(p1, p2) -> do
            let dist = distPoi (Variable v) p1 p2 scheme
            putStrLn $ "distPoi(" ++ v ++ ", " ++ show p1 ++ ", " ++ show p2 ++ ") = " ++ show dist
    putStrLn "---------------------"
    forM_ ["a", "b", "c", "d"] $ \v1 -> do
        forM_ (pre (Variable v1) scheme) $ \v2 -> do
            let ps = Points.boundaries v2 scheme
            forM_ (zip ps (drop 1 ps)) $ \(p1, p2) -> do
                let dist = distPoi' p1 p2 scheme v2 (Variable v1)
                putStrLn $ "distPoi'(" ++ show v2 ++ ", " ++ v1 ++ ", " ++ show p1 ++ ", " ++ show p2 ++ ") = " ++ show dist
    putStrLn "====================="
    forM_ ["a", "b", "c", "d"] $ \v -> do
        forM_ (Points.boundaries (Variable v) scheme) $ \p -> do
            let dist = getOriginalPoint (Variable v) p scheme
            putStrLn $ "getOriginalPoint(" ++ v ++ ", " ++ show p ++ ") = " ++ show dist
    putStrLn "====================="
    putStrLn "====================="
    putStrLn "====================="
    let formula = phi scheme
    print $ length formula
    -- putStrLn "starting to solve"
    -- forM_ (solvePhi formula) $ \st -> do 
    --     print st
