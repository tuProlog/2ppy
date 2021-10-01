from tuprolog import logger
# noinspection PyUnresolvedReferences
import jpype.imports
# noinspection PyUnresolvedReferences
import it.unibo.tuprolog.solve.stdlib.rule as _rule
from tuprolog.solve import signature


KtAppend = _rule.Append

Arrow = _rule.Arrow

CurrentPrologFlag = _rule.CurrentPrologFlag

KtMember = _rule.Member

Not = _rule.Not

Once = _rule.Once

KtSemicolon = _rule.Semicolon

SetPrologFlag = _rule.SetPrologFlag


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
