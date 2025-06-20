{-# LANGUAGE DeriveGeneric #-}

module Types
  ( Behaviour(..)
  , Interval(..)
  , Variable(..)
  , Statement(..)
  ) where

import GHC.Generics
import Data.Aeson (encode, ToJSON, FromJSON)

data Behaviour = MONO | ANTI | CONST | ARB
    deriving (Eq, Generic)

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
instance FromJSON Behaviour
instance FromJSON Interval
instance FromJSON Variable
instance FromJSON Statement

instance Show Behaviour where
    show MONO  = "mono"
    show ANTI  = "anti"
    show CONST = "const"
    show ARB   = "arb"

instance Show Statement where 
    show (Statement (Variable a) (Interval x y) q (Interval l u) (Variable b)) =
        concat ["(", show a, " [", show x, ",", show y, "] ", show q, " [", show l, ",", show u, "] ", show b, ")"]
