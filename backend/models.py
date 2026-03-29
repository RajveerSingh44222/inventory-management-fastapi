from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name of the product"
    )
    description: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Short description of the product"
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price of the product, must be greater than 0"
    )
    quantity: int = Field(
        ...,
        ge=0,
        description="Available stock quantity, must be 0 or more"
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)