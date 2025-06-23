module Scheme.Normalise where

import Types 
  ( Behaviour(..)
  , Interval(..)
  , mkInterval
  , Statement(..)
  , Scheme(..)
  , Variable(..)
  )
import qualified Scheme.Points as Points
import qualified Scheme.Rules  as Rules

import Data.Map (Map)
import qualified Data.Map as Map
import qualified Data.Maybe as Maybe

normalise :: Scheme -> Scheme
normalise (Scheme m) =
  Scheme
    . Map.mapWithKey
        (\k m' ->
           Map.map
             (minimalHeight . gapFree . overlapFree (Points.boundaries k (Scheme m)))
             m')
    $ m

overlapFree :: [Double] -> [Statement] -> [Statement]
overlapFree bds sts = Maybe.catMaybes $ zipWith mergeStatements bds . drop 1 $ bds
  where
    mergeStatements x y =
      Rules.isect (mkInterval x y) . Points.overlaps (mkInterval x y) $ sts

gapFree :: [Statement] -> [Statement]
gapFree [] = []
gapFree [x] = [x]
gapFree (x:y:xs) =
  case compare ((end . domain) x) ((start . domain) y) of
    EQ -> x : gapFree (y : xs)
    LT -> error "Gap found between statements"
    GT -> error "Statements are not sorted by domain"

minimalHeight :: [Statement] -> [Statement]
minimalHeight [] = []
minimalHeight [x] = [x]
minimalHeight (st:sts) = minimalHeight' [st] sts
  where
    minimalHeight' :: [Statement] -> [Statement] -> [Statement]
    minimalHeight' [] (x:xs) = minimalHeight' [x] xs
    minimalHeight' xs [] = reverse xs
    minimalHeight' (x:xs) (y:ys) =
      let (x', y', changed) = applyRules x y
       in if changed
            then minimalHeight' xs (x' : y' : ys)
            else minimalHeight' (y' : x' : xs) ys

applyRules :: Statement -> Statement -> (Statement, Statement, Bool)
applyRules st1 st2 = (st1', st2', result1 || result2)
  where
    st1' = Rules.leftRule st1 st2
    st2' = Rules.rightRule st1 st2
    result1 = st1 /= st1'
    result2 = st2 /= st2'

