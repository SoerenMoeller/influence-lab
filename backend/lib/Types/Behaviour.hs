{-# LANGUAGE DeriveGeneric #-}

module Types.Behaviour
  ( Behaviour(..)
  , join2
  , meet2
  , join
  , meet
  ) where

import Data.Aeson (FromJSON, ToJSON, encode)
import Data.List (foldl')
import Data.PartialOrd hiding ((==))
import GHC.Generics

data Behaviour
  = MONO
  | ANTI
  | CONST
  | ARB
  deriving (Eq, Generic)

instance PartialOrd Behaviour where
  _ <= CONST = True
  ARB <= _ = True
  x <= y = x == y

instance Show Behaviour where
  show MONO = "mono"
  show ANTI = "anti"
  show CONST = "const"
  show ARB = "arb"

instance ToJSON Behaviour
instance FromJSON Behaviour

join2 :: Behaviour -> Behaviour -> Behaviour
join2 x y =
  if x Data.PartialOrd.<= y
    then y
    else CONST

meet2 :: Behaviour -> Behaviour -> Behaviour
meet2 x y =
  if x Data.PartialOrd.<= y
    then x
    else ARB

join :: [Behaviour] -> Behaviour
join = foldl' join2 ARB

meet :: [Behaviour] -> Behaviour
meet = foldl' meet2 CONST
