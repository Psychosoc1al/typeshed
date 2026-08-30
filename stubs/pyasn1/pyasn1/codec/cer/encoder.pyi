from _typeshed import Unused
from collections.abc import Callable
from typing import Any, ClassVar, Literal, SupportsBytes, overload

from pyasn1.codec.ber import encoder
from pyasn1.type.base import Asn1Type, SimpleAsn1Type
from pyasn1.type.tag import TagSet
from pyasn1.type.univ import OctetString, SequenceOfAndSetOfBase

__all__ = ["Encoder", "encode"]

class BooleanEncoder(encoder.IntegerEncoder):
    @overload
    def encodeValue(
        self, value: Literal[0, False], asn1Spec: Unused, encodeFun: Unused, **options: Unused
    ) -> tuple[tuple[Literal[0]], Literal[False], Literal[False]]: ...
    @overload
    def encodeValue(
        self, value: Literal[1, True], asn1Spec: Unused, encodeFun: Unused, **options: Unused
    ) -> tuple[tuple[Literal[255]], Literal[False], Literal[False]]: ...
    @overload
    def encodeValue(
        self,
        value: Any,  # Technically, everything not equal to `0` will return `(255,), False, False`
        asn1Spec: Unused,
        encodeFun: Unused,
        **options: Unused,
    ) -> tuple[tuple[Literal[0, 255]], Literal[False], Literal[False]]: ...

class RealEncoder(encoder.RealEncoder): ...

class TimeEncoderMixIn:
    Z_CHAR: ClassVar[int] = 90
    PLUS_CHAR: ClassVar[int] = 43
    MINUS_CHAR: ClassVar[int] = 45
    COMMA_CHAR: ClassVar[int] = 44
    DOT_CHAR: ClassVar[int] = 46
    ZERO_CHAR: ClassVar[int] = 48
    MIN_LENGTH: ClassVar[int] = 12
    MAX_LENGTH: ClassVar[int] = 19

    @overload
    def encodeValue(
        self,
        value: OctetString,
        asn1Spec: None,
        encodeFun: Callable[[bytes, OctetString, dict[str, Any]], bytes],  # `Any` as `encodeFun` is user-defined
        **options: dict[str, Any],  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, bool, Literal[True]]: ...
    @overload
    def encodeValue(
        self,
        value: str | bytes | SimpleAsn1Type | SupportsBytes,
        asn1Spec: OctetString,
        encodeFun: Callable[[bytes, OctetString, dict[str, Any]], bytes],  # `Any` as `encodeFun` is user-defined
        **options: dict[str, Any],  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, bool, Literal[True]]: ...

class GeneralizedTimeEncoder(TimeEncoderMixIn, encoder.OctetStringEncoder):
    MIN_LENGTH: ClassVar[int] = 12
    MAX_LENGTH: ClassVar[int] = 20

class UTCTimeEncoder(TimeEncoderMixIn, encoder.OctetStringEncoder):
    MIN_LENGTH: ClassVar[int] = 10
    MAX_LENGTH: ClassVar[int] = 14

class SetOfEncoder(encoder.SequenceOfEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options): ...

class SequenceOfEncoder(encoder.SequenceOfEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options): ...

class SetEncoder(encoder.SequenceEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options): ...

class SequenceEncoder(encoder.SequenceEncoder):
    omitEmptyOptionals: bool

TAG_MAP: dict[TagSet, encoder.AbstractItemEncoder]
TYPE_MAP: dict[int, encoder.AbstractItemEncoder]
# deprecated aliases
tagMap = TAG_MAP
typeMap = TYPE_MAP

class SingleItemEncoder(encoder.SingleItemEncoder):
    fixedDefLengthMode: bool
    fixedChunkSize: int

    TAG_MAP: dict[TagSet, encoder.AbstractItemEncoder]
    TYPE_MAP: dict[int, encoder.AbstractItemEncoder]

class Encoder(encoder.Encoder):
    SINGLE_ITEM_ENCODER: type[SingleItemEncoder]

encode: Encoder
