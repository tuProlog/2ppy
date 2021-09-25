from tuprolog import logger

# noinspection PyUnresolvedReferences
import jpype
# noinspection PyUnresolvedReferences
import jpype.imports

# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Append as KtAppend
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Arrow
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import CurrentPrologFlag
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Member as KtMember
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Not
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Once
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import Semicolon as KtSemicolon
# noinspection PyUnresolvedReferences
from it.unibo.tuprolog.solve.stdlib.rule import SetPrologFlag

from tuprolog.solve import signature


class Append:
    FUNCTOR = KtAppend.FUNCTOR

    ARITY = KtAppend.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = KtAppend.Base.INSTANCE

    Recursive = KtAppend.Recursive.INSTANCE


Arrow = Arrow.INSTANCE

CurrentPrologFlag = CurrentPrologFlag.INSTANCE


class Member:
    FUNCTOR = KtMember.FUNCTOR

    ARITY = KtMember.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = KtMember.Base.INSTANCE

    Recursive = KtMember.Recursive.INSTANCE


Not = Not.INSTANCE

Once = Once.INSTANCE


class Semicolon:
    FUNCTOR = KtSemicolon.FUNCTOR

    ARITY = KtSemicolon.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    class If:
        Then = KtSemicolon.If.Then.INSTANCE

        Else = KtSemicolon.If.Else.INSTANCE

    class Or:
        Left = KtSemicolon.Or.Left.INSTANCE

        Right = KtSemicolon.Or.Right.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.rule.*")
