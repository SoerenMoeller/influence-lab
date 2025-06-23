module Scheme.IO where

import Types
  ( Behaviour(ANTI, ARB, CONST, MONO)
  , Interval(..)
  , mkInterval
  , LongStatement(..)
  , Scheme(..)
  , Statement(..)
  , StatementList
  , Variable(..)
  )

import Data.Map (Map)
import qualified Data.Map as Map
import qualified Data.Aeson as Aeson
import qualified Data.ByteString.Lazy.Char8 as B
import qualified System.Environment as SysEnv


tuplesToStatements ::
     [(String, (Double, Double), Behaviour, (Double, Double), String)]
  -> StatementList
tuplesToStatements =
  map
    (\(a, (x, y), q, (l, u), b) ->
       LongStatement (Variable a) (mkInterval x y) q (mkInterval l u) (Variable b))

statementListToScheme :: StatementList -> Scheme
statementListToScheme sts = Scheme $ foldr insertStatement Map.empty sts
  where
    insertStatement (LongStatement varA dom beh rng varB) acc =
      let innerMap = Map.findWithDefault Map.empty varA acc
          updatedList =
            Statement dom beh rng : Map.findWithDefault [] varB innerMap
          updatedInnerMap = Map.insert varB updatedList innerMap
       in Map.insert varA updatedInnerMap acc

schemeToStatementList :: Scheme -> StatementList
schemeToStatementList (Scheme m) =
  [ LongStatement varA dom beh rng varB
  | (varA, innerMap) <- Map.toList m
  , (varB, stmts) <- Map.toList innerMap
  , Statement dom beh rng <- stmts
  ]

schemeToJson :: Scheme -> B.ByteString
schemeToJson = Aeson.encode . schemeToStatementList 

schemeFromJson :: IO (Maybe Scheme)        
schemeFromJson = do
    args <- SysEnv.getArgs
    case args of
        [jsonStr] -> do
            case statements of
                Just sts -> return . Just $ statementListToScheme sts
                Nothing  -> return Nothing 
              where
                statements = Aeson.decode (B.pack jsonStr) :: Maybe [LongStatement]
        _ -> return Nothing 
