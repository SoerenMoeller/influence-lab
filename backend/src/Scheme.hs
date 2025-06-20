import Types (Behaviour(MONO, ANTI, ARB, CONST), Interval(..), Variable(..), Statement(..))
import Data.Aeson (encode)

listToStatement :: [(String, (Double, Double), Behaviour, (Double, Double), String)] 
    -> [Statement]
listToStatement [] = []
listToStatement ((a, (x, y), q, (l, u), b):xs) =
    Statement (Variable a) (Interval x y) q (Interval l u) (Variable b) : listToStatement xs

exampleData :: [Statement]
exampleData = listToStatement 
    [     
        ("a", (1, 2), MONO, (3, 4), "b")
    ]

main :: IO ()
main = do
    let statements = encode exampleData
    print statements
