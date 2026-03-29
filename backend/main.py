from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from database_model import Base, Product as DBProduct
from models import ProductCreate, ProductUpdate, ProductResponse

app = FastAPI(
    title="Product Management API",
    description="A REST API for managing products using FastAPI, SQLAlchemy, and MySQL.",
    version="1.0.0"
)

# Create table automatically
Base.metadata.create_all(bind=engine)


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/home",
    summary="Home route",
    description="Simple route to test whether the API is running.",
    tags=["Home"]
)
def greet():
    return {"message": "hello srm"}


# Get all products with sorting and filtering
@app.get(
    "/products",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all products",
    description="Returns all products. Supports sorting and optional filtering.",
    tags=["Products"]
)
def get_all_products(
    sort_by: str = Query(
        "id",
        description="Sort by: id, name, price, quantity"
    ),
    order: str = Query(
        "asc",
        description="Sort order: asc or desc"
    ),
    min_price: float | None = Query(
        None,
        ge=0,
        description="Minimum price filter"
    ),
    max_price: float | None = Query(
        None,
        ge=0,
        description="Maximum price filter"
    ),
    in_stock: bool | None = Query(
        None,
        description="Filter only products that are in stock"
    ),
    db: Session = Depends(get_db)
):
    query = db.query(DBProduct)

    # Filtering
    if min_price is not None:
        query = query.filter(DBProduct.price >= min_price)

    if max_price is not None:
        query = query.filter(DBProduct.price <= max_price)

    if in_stock is True:
        query = query.filter(DBProduct.quantity > 0)

    # Sorting
    allowed_sort_fields = {
        "id": DBProduct.id,
        "name": DBProduct.name,
        "price": DBProduct.price,
        "quantity": DBProduct.quantity
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort_by field. Use id, name, price, or quantity."
        )

    column = allowed_sort_fields[sort_by]

    if order.lower() == "desc":
        query = query.order_by(column.desc())
    elif order.lower() == "asc":
        query = query.order_by(column.asc())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order value. Use asc or desc."
        )

    return query.all()


# Get one product by id
@app.get(
    "/products/{id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get product by ID",
    description="Returns a single product by its ID.",
    tags=["Products"]
)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# Add new product
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
    description="Creates a new product in the database.",
    tags=["Products"]
)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = DBProduct(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


# Update product
@app.put(
    "/products/{id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a product",
    description="Updates an existing product by its ID.",
    tags=["Products"]
)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    existing_product = db.query(DBProduct).filter(DBProduct.id == id).first()

    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    try:
        existing_product.name = product.name
        existing_product.description = product.description
        existing_product.price = product.price
        existing_product.quantity = product.quantity

        db.commit()
        db.refresh(existing_product)
        return existing_product
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )


# Delete product
@app.delete(
    "/products/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product",
    description="Deletes a product by its ID.",
    tags=["Products"]
)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    try:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )