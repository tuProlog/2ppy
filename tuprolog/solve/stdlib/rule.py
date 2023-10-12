from tuprolog import logger
from tuprolog.solve import signature
import jpype.imports  # noqa: F401
import it.unibo.tuprolog.solve.stdlib.rule as _rule  # type: ignore


_Append = _rule.Append


class Append:
    FUNCTOR = _Append.FUNCTOR

    ARITY = _Append.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = _Append.Base.INSTANCE

    Recursive = _Append.Recursive.INSTANCE


Arrow : _rule.Arrow = _rule.Arrow.INSTANCE


CurrentPrologFlag : _rule.CurrentPrologFlag = _rule.CurrentPrologFlag.INSTANCE


_Member = _rule.Member


class Member:
    FUNCTOR = _Member.FUNCTOR

    ARITY = _Member.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    Base = _Member.Base.INSTANCE

    Recursive = _Member.Recursive.INSTANCE


Not : _rule.Not = _rule.Not.INSTANCE


Once : _rule.Once = _rule.Once.INSTANCE


_Semicolon = _rule.Semicolon


class Semicolon:
    FUNCTOR = _Semicolon.FUNCTOR

    ARITY = _Semicolon.ARITY

    SIGNATURE = signature(FUNCTOR, ARITY)

    class If:
        Then = _Semicolon.If.Then.INSTANCE

        Else = _Semicolon.If.Else.INSTANCE

    class Or:
        Left = _Semicolon.Or.Left.INSTANCE

        Right = _Semicolon.Or.Right.INSTANCE


SetPrologFlag : _rule.SetPrologFlag = _rule.SetPrologFlag.INSTANCE


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.stdlib.rule.*")
