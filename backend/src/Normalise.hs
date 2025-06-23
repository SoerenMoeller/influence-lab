import Types
  ( Behaviour(ANTI, ARB, CONST, MONO)
  , Interval(..)
  , Statement(..)
  , Variable(..)
  )
import qualified Scheme.IO as IO
import qualified Scheme.Normalise as Normalise

import qualified Data.Maybe as Maybe
import Control.Monad (guard)

main :: IO ()
main = do
    input <- IO.schemeFromJson
    guard (Maybe.isJust input)
    let scheme = Maybe.fromJust input
    print . IO.schemeToJson . Normalise.normalise $ scheme
