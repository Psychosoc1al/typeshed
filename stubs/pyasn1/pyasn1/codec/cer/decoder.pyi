from _typeshed import Unused
from collections.abc import Generator
from typing import Any, Literal, TypeVar, overload

from pyasn1 import error
from pyasn1.codec.ber import decoder
from pyasn1.codec.streaming import _ReadSeekable
from pyasn1.type import base, tag, univ

__all__ = ["decode", "StreamingDecoder"]

_T = TypeVar("_T", bound=base.Asn1Type)

class BooleanPayloadDecoder(decoder.AbstractSimplePayloadDecoder):
    protoComponent: univ.Boolean

    @overload
    def valueDecoder(
        self,
        substrate: _ReadSeekable,
        asn1Spec: None,
        tagSet: tag.TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options: dict[str, Any],  # `options` are passed to `codec.streaming.readFromStream()`
    ) -> Generator[error.SubstrateUnderrunError | Literal[1, 0] | univ.Boolean]: ...
    @overload
    def valueDecoder(
        self,
        substrate: _ReadSeekable,
        asn1Spec: _T,
        tagSet: tag.TagSet | None = None,
        length: int | None = None,
        state: Unused = None,
        decodeFun: Unused = None,
        substrateFun: Unused = None,
        **options: dict[str, Any],  # `options` are passed to `codec.streaming.readFromStream()`
    ) -> Generator[error.SubstrateUnderrunError | Literal[1, 0] | _T]: ...

BitStringPayloadDecoder = decoder.BitStringPayloadDecoder
OctetStringPayloadDecoder = decoder.OctetStringPayloadDecoder
RealPayloadDecoder = decoder.RealPayloadDecoder

TAG_MAP: dict[tag.TagSet, decoder.AbstractPayloadDecoder]
TYPE_MAP: dict[int, decoder.AbstractPayloadDecoder]
# deprecated aliases
tagMap = TAG_MAP
typeMap = TYPE_MAP

class SingleItemDecoder(decoder.SingleItemDecoder):
    TAG_MAP: dict[tag.TagSet, decoder.AbstractPayloadDecoder]
    TYPE_MAP: dict[int, decoder.AbstractPayloadDecoder]

class StreamingDecoder(decoder.StreamingDecoder):
    SINGLE_ITEM_DECODER: type[SingleItemDecoder]

class Decoder(decoder.Decoder):
    STREAMING_DECODER: type[StreamingDecoder]

decode: Decoder
