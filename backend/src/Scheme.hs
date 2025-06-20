import Types (Behaviour(MONO, ANTI, ARB, CONST), Interval(..), Variable(..), Statement(..))
import Data.Aeson (encode)
import Data.List (sort, foldl', nub)

listToStatement :: [(String, (Double, Double), Behaviour, (Double, Double), String)]
    -> [Statement]
listToStatement [] = []
listToStatement ((a, (x, y), q, (l, u), b):xs) =
    Statement (Variable a) (Interval x y) q (Interval l u) (Variable b) : listToStatement xs

exampleData :: [Statement]
exampleData = normalise . listToStatement $
    [
        ("a", (1, 2), MONO, (3, 4), "b"),
        ("a", (1.5, 3), MONO, (3, 5), "b"),
        ("a", (3, 5), CONST, (4, 5), "b")
    ]

boundaries :: Variable -> [Statement] -> [Double]
boundaries var sts = nub $ bdsFrom ++ bdsTo
  where
    bdsFrom = concatMap (\(Statement _ (Interval x y) _ _ _) -> [x, y])
            . filter ((==) var . variableFrom)
            $ sts
    bdsTo = concatMap (\(Statement _ _ _ (Interval l u) _) -> [l, u])
          . filter ((==) var . variableTo)
          $ sts

overlaps :: Interval -> [Statement] -> [Statement]
overlaps (Interval x y) =
    filter (\(Statement _ (Interval x' y') _ _ _) -> x' <= x && y' >= y)

intersectBehaviors :: Behaviour -> Behaviour -> Behaviour
intersectBehaviors MONO ANTI = CONST
intersectBehaviors ANTI MONO = CONST
intersectBehaviors CONST _   = CONST
intersectBehaviors _ CONST   = CONST
intersectBehaviors ARB x     = x
intersectBehaviors x ARB     = x
intersectBehaviors x y       = x

statementIntersection :: Interval -> Variable -> Variable -> [Statement] -> Statement
statementIntersection dom varA varB sts = Statement varA dom beh rng varB
  where
    rng = Interval
        (maximum . map (start . range) $ sts)
        (minimum . map (end . range) $ sts)
    beh = foldl' (\acc (Statement _ _ b _ _) -> intersectBehaviors acc b) ARB sts

normalise :: [Statement] -> [Statement]
normalise sts =
    zipWith (\ x y
  -> statementIntersection
       (Interval x y) (Variable "a") (Variable "b")
       . overlaps (Interval x y)
       $ sts) bds $ drop 1 bds
  where
    bds :: [Double]
    bds = sort . boundaries (Variable "a") $ sts

main :: IO ()
main = do
    let statements = encode exampleData
    print statements
