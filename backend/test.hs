
{-# LANGUAGE DeriveGeneric #-}

import GHC.Generics
import Data.Aeson (encode, ToJSON)

data Behaviour = MONO | ANTI | CONST | ARB
    deriving (Eq, Generic)

instance Show Behaviour where
    show MONO  = "mono"
    show ANTI  = "anti"
    show CONST = "const"
    show ARB   = "arb"

data Interval = Interval
    { start :: Double
    , end   :: Double
    } deriving (Show, Eq, Generic) 

newtype Variable = Variable String 
    deriving (Show, Eq, Generic)

data Statement = Statement
    { variableFrom :: Variable
    , domain :: Interval
    , behaviour :: Behaviour
    , range :: Interval
    , variableTo :: Variable
    } deriving (Generic, Eq)

instance ToJSON Behaviour
instance ToJSON Interval
instance ToJSON Variable
instance ToJSON Statement

instance Show Statement where 
    show (Statement (Variable a) (Interval x y) q (Interval l u) (Variable b)) =
        concat ["(", ")", "()"]

listToStatement :: [(String, (Double, Double), String, (Double, Double), String)] 
    -> [Statement]
listToStatement [] = []
listToStatement ((a, (x, y), q, (l, u), b):xs) =
    Statement (Variable a) (Interval x y) (strToBehavior q) (Interval l u) (Variable b) : listToStatement xs
  where
    strToBehavior :: String -> Behaviour 
    strToBehavior "mono" = MONO
    strToBehavior "anti" = ANTI
    strToBehavior "const" = CONST
    strToBehavior "arb" = ARB

exampleData :: [Statement]
exampleData = listToStatement 
    [     
        ("a", (1, 2), "mono", (3, 4), "b")
    ]

main :: IO ()
main = do
    let statements = encode exampleData
    print statements
