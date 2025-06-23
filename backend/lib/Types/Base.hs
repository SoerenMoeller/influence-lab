{-# LANGUAGE DeriveGeneric #-}

module Types.Base
  ( Interval(..)
  , mkInterval
  , Variable(..)
  ) where

import Data.Aeson (FromJSON, ToJSON, encode)
import GHC.Generics
import GHC.Stack (HasCallStack)

data Interval = Interval
  { start :: Double
  , end :: Double
  } deriving (Show, Eq, Generic)


mkInterval :: HasCallStack => Double -> Double -> Interval
mkInterval s e
  | s <= e = Interval s e
  | otherwise = error $ "normalise: Could not create Interval: start must be ≤ end. Got start="
                     ++ show s ++ ", end=" ++ show e

newtype Variable =
  Variable String
  deriving (Eq, Generic, Ord)

instance Show Variable where
  show (Variable v) = v

instance ToJSON Interval

instance ToJSON Variable

instance FromJSON Interval

instance FromJSON Variable
