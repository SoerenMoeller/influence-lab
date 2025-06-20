import Types (Behaviour(MONO, ANTI, ARB, CONST), Interval(..), Variable(..), Statement(..))

import Data.Aeson (decode)
import System.Environment (getArgs)
import qualified Data.ByteString.Lazy.Char8 as B


{-# LANGUAGE OverloadedStrings #-}

main :: IO ()
main = do 
    args <- getArgs
    case args of
      [jsonStr] -> do
          let statements = decode (B.pack jsonStr) :: Maybe [Statement]
          case statements of
              Just stmts -> mapM_ print stmts
              Nothing    -> putStrLn "Failed to parse JSON into [Statement]"
      _ -> putStrLn "Usage: GetScheme \"[JSON array of Statements]\""
