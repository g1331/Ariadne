"""用于 Ariadne 数据模型的工具类."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, Union
from typing_extensions import NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict, field_serializer

from ..util import snake_to_camel

if TYPE_CHECKING:
    from ..typing import AbstractSetIntStr, DictStrAny, MappingIntStrAny


class AriadneBaseModel(BaseModel):
    """Ariadne 一切数据模型的基类."""

    def __init__(self, **data: Any) -> None:
        """初始化模型. 直接向 pydantic 转发."""
        super().__init__(**data)

    def dict(
        self,
        *,
        include: Union[None, "AbstractSetIntStr", "MappingIntStrAny"] = None,
        exclude: Union[None, "AbstractSetIntStr", "MappingIntStrAny"] = None,
        by_alias: bool = False,
        skip_defaults: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        to_camel: bool = False,
    ) -> "DictStrAny":
        """转化为字典, 直接向 pydantic 转发."""
        _, *_ = by_alias, exclude_none, skip_defaults
        data = self.model_dump(
            include=include,  # type: ignore
            exclude=exclude,  # type: ignore
            by_alias=True,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=True,
        )
        if to_camel:
            data = {snake_to_camel(k): v for k, v in data.items()}
        return data

    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
    )

    @field_serializer("*", mode="wrap")
    def _serialize_datetime(self, value, handler, info):
        """序列化 datetime 对象为时间戳"""
        if isinstance(value, datetime):
            return int(value.timestamp())
        return handler(value)


class AriadneOptions(TypedDict):
    """Ariadne 内部的选项存储"""

    installed_log: NotRequired[Literal[True]]
    inject_bypass_listener: NotRequired[Literal[True]]
    default_account: NotRequired[int]
