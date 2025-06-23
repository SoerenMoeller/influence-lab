module Scheme.Rules where

import Types 
  ( Behaviour(..)
  , Interval(..)
  , mkInterval
  , Statement(..)
  , Scheme(..)
  , Variable(..)
  )
import Types.Behaviour (join)

isect :: Interval -> [Statement] -> Maybe Statement
isect dom [] = Nothing
isect dom sts = Just $ Statement dom beh rng
  where
    rng =
      mkInterval
        (maximum . map (start . range) $ sts)
        (minimum . map (end . range) $ sts)
    beh = join . map behaviour $ sts

leftRule :: Statement -> Statement -> Statement
leftRule st1 st2 =
  case behaviour st1 of
    MONO -> Statement (domain st1) MONO (mkInterval l (min u u'))
    ANTI -> Statement (domain st1) ANTI (mkInterval (max l l') u)
    CONST -> Statement (domain st1) CONST (mkInterval (max l l') (min u u'))
    ARB -> st1
  where
    (l, u) = (start . range $ st1, end . range $ st1)
    (l', u') = (start . range $ st2, end . range $ st2)

rightRule :: Statement -> Statement -> Statement
rightRule st1 st2 =
  case behaviour st2 of
    MONO  -> Statement (domain st2) MONO  (mkInterval (max l l') u')
    ANTI  -> Statement (domain st2) ANTI  (mkInterval l' (min u u'))
    CONST -> Statement (domain st2) CONST (mkInterval (max l l') (min u u'))
    ARB   -> st2
  where
    (l, u) = (start . range $ st1, end . range $ st1)
    (l', u') = (start . range $ st2, end . range $ st2)
