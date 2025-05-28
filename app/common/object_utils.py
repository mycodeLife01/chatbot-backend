from pydantic import BaseModel


# def to_response(raw):
#     if isinstance(raw, list):
#         if not raw:
#             return []
#         response_cls_name = type(raw[0]).__name__ + "Response"
#         response_cls = globals().get(response_cls_name)
#         if response_cls is None:
#             return None
#         return [response_cls(**obj.model_dump()) for obj in raw]
#     elif isinstance(raw, BaseModel):
#         response_cls_name = type(raw).__name__ + "Response"
#         response_cls = globals().get(response_cls_name)
#         if response_cls is None:
#             return None
#         return response_cls(**raw.model_dump())
#     return None
