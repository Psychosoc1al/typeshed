from _typeshed import Unused
from collections.abc import Iterable
from typing import Any, ClassVar, Literal, Protocol, SupportsBytes, TypeVar, overload, type_check_only

from pyasn1.codec.ber import encoder
from pyasn1.type import base, tag, univ

__all__ = ["Encoder", "encode"]

_T = TypeVar("_T")
_ValueT_contra = TypeVar("_ValueT_contra", contravariant=True)
_SpecT_contra = TypeVar("_SpecT_contra", contravariant=True)

@type_check_only
class _EncodeFun(Protocol[_ValueT_contra, _SpecT_contra]):
    def __call__(
        self,
        value: _ValueT_contra,
        asn1Spec: _SpecT_contra,
        **options: Any,  # `Any` as this may be a user-defined function
    ) -> bytes: ...

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
        value: univ.OctetString,
        asn1Spec: None,
        encodeFun: _EncodeFun[bytes, univ.OctetString],
        **options: Any,  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, bool, Literal[True]]: ...
    @overload
    def encodeValue(
        self,
        value: str | bytes | base.SimpleAsn1Type | SupportsBytes,
        asn1Spec: univ.OctetString,
        encodeFun: _EncodeFun[bytes, univ.OctetString],
        **options: Any,  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, bool, Literal[True]]: ...

class GeneralizedTimeEncoder(TimeEncoderMixIn, encoder.OctetStringEncoder):
    MIN_LENGTH: ClassVar[int] = 12
    MAX_LENGTH: ClassVar[int] = 20

class UTCTimeEncoder(TimeEncoderMixIn, encoder.OctetStringEncoder):
    MIN_LENGTH: ClassVar[int] = 10
    MAX_LENGTH: ClassVar[int] = 14

class SetOfEncoder(encoder.SequenceOfEncoder):
    @overload
    def encodeValue(
        self,
        value: univ.SequenceOfAndSetOfBase,
        asn1Spec: None,
        encodeFun: _EncodeFun[base.Asn1Type | bytes, base.Asn1Type | None],
        **options: Any,  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, Literal[True], Literal[True]]: ...
    @overload
    def encodeValue(
        self,
        value: Iterable[_T],
        asn1Spec: univ.SequenceOfAndSetOfBase,
        encodeFun: _EncodeFun[_T | bytes, base.Asn1Type | None],
        **options: Any,  # `options` are passed to `encodeFun()`
    ) -> tuple[bytes, Literal[True], Literal[True]]: ...

class SequenceOfEncoder(encoder.SequenceOfEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options): ...

class SetEncoder(encoder.SequenceEncoder):
    def encodeValue(self, value, asn1Spec, encodeFun, **options): ...

class SequenceEncoder(encoder.SequenceEncoder):
    omitEmptyOptionals: bool

TAG_MAP: dict[tag.TagSet, encoder.AbstractItemEncoder]
TYPE_MAP: dict[int, encoder.AbstractItemEncoder]
# deprecated aliases
tagMap = TAG_MAP
typeMap = TYPE_MAP

class SingleItemEncoder(encoder.SingleItemEncoder):
    fixedDefLengthMode: bool
    fixedChunkSize: int

    TAG_MAP: dict[tag.TagSet, encoder.AbstractItemEncoder]
    TYPE_MAP: dict[int, encoder.AbstractItemEncoder]

class Encoder(encoder.Encoder):
    SINGLE_ITEM_ENCODER: type[SingleItemEncoder]

encode: Encoder
