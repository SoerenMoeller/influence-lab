import Types
  ( Behaviour(ANTI, ARB, CONST, MONO)
  , Interval(..)
  , Scheme(..)
  , Statement(..)
  , Variable(..)
  )
import qualified Scheme.IO as IO
import qualified Scheme.Normalise as Normalise

exampleData :: Scheme
exampleData =
  IO.statementListToScheme . IO.tuplesToStatements
    $ [ ("a", (0, 2), ANTI, (3, 3.5), "b")
      , ("a", (2, 3.3), ANTI, (2.1, 3.2), "b")
      , ("a", (3, 4.5), ANTI, (1.4, 2.2), "b")
      , ("a", (4, 5.1), ANTI, (1.2, 2), "b")
      , ("a", (5, 7), MONO, (1.1, 1.9), "b")
      , ("a", (7, 8), CONST, (1.7, 3), "b")
      , ("a", (7.9, 9), ANTI, (1, 2), "b")
      , ("a", (8.6, 10.8), MONO, (1.5, 1.8), "b")
      , ("a", (8.6, 10.7), ANTI, (1.6, 2.2), "b")
      , ("a", (10, 11), ANTI, (1.3, 1.9), "b")
      ]

main :: IO ()
main = print . IO.schemeToJson $ exampleData
