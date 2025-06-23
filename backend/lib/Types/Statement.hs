{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE DuplicateRecordFields #-}

module Types.Statement where

import Data.Aeson (FromJSON, ToJSON, encode)
import Data.Map (Map)
import qualified Data.Map as Map
import qualified Data.Maybe as Maybe
import GHC.Generics
import Types.Base (Interval(..), mkInterval, Variable(..))
import Types.Behaviour (Behaviour(..))

data LongStatement = LongStatement
  { variableFrom :: Variable
  , domain :: Interval
  , behaviour :: Behaviour
  , range :: Interval
  , variableTo :: Variable
  } deriving (Generic, Eq)

instance ToJSON LongStatement

instance FromJSON LongStatement

type StatementList = [LongStatement]

instance Show LongStatement where
  show (LongStatement (Variable a) (Interval x y) q (Interval l u) (Variable b)) =
    concat
      [ "("
      , show a
      , " ["
      , show x
      , ","
      , show y
      , "] "
      , show q
      , " ["
      , show l
      , ","
      , show u
      , "] "
      , show b
      , ")"
      ]

data Statement = Statement
  { domain :: Interval
  , behaviour :: Behaviour
  , range :: Interval
  } deriving (Generic, Eq)

instance Show Statement where
  show (Statement (Interval x y) q (Interval l u)) =
    concat
      [ "( ["
      , show x
      , ","
      , show y
      , "] "
      , show q
      , " ["
      , show l
      , ","
      , show u
      , "] )"
      ]

newtype Scheme =
  Scheme (Map Variable (Map Variable [Statement]))

instance Show Scheme where
  show (Scheme m) = concat result
    where
      result =
        [ "(" ++ show a ++ ", " ++ show b ++ ") -> " ++ show sts ++ "\n"
        | (a, innerMap) <- Map.toList m
        , (b, sts) <- Map.toList innerMap
        ]
