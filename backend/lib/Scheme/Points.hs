module Scheme.Points where

import Types 
  ( Behaviour(..)
  , Interval(..)
  , Statement(..)
  , Scheme(..)
  , Variable(..)
  )

import Data.Map (Map)
import qualified Data.Map as Map
import Data.Maybe as Maybe
import Data.List (nub, sort)

boundaries :: Variable -> Scheme -> [Double]
boundaries var sts = sort . nub $ bdsOuter ++ bdsInner
  where
    bdsOuter =
      concatMap (\(Statement (Interval x y) _ _) -> [x, y])
        $ statementInflFrom var sts
    bdsInner =
      concatMap (\(Statement _ _ (Interval x y)) -> [x, y])
        $ statementInflTo var sts

statementInflFrom :: Variable -> Scheme -> [Statement]
statementInflFrom v (Scheme m) =
  concat . Map.elems $ Map.findWithDefault Map.empty v m

statementInflTo :: Variable -> Scheme -> [Statement]
statementInflTo v (Scheme m) = concat . Maybe.mapMaybe (Map.lookup v) $ Map.elems m

overlaps :: Interval -> [Statement] -> [Statement]
overlaps (Interval x y) =
  filter (\(Statement (Interval x' y') _ _) -> x' <= x && y' >= y)

