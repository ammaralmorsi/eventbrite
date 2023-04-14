from typing import List
from fastapi import APIRouter
from starlette.responses import PlainTextResponse
from .db import driver, models

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

db_categories_driver = driver.CategoriesDriver()


@router.post(
    "/",
    summary="Create a new category",
    description="This endpoint allows you to create a new category in the database.",
    tags=["categories"],
    responses={
        200: {"description": "Category created successfully"},
    },
)
async def create_category(category: models.Category):
    """
    Create a new category in the database.

    Args:
        category (models.Category): The category object to be created.

    Returns:
        PlainTextResponse: A plain text response indicating successful creation of category.
    """
    db_categories_driver.insert(category.dict())
    return PlainTextResponse("Category created successfully", status_code=200)


@router.get(
    "/",
    summary="Get all categories",
    description="This endpoint allows you to get all categories in the database.",
    tags=["categories"],
    responses={
        200: {"description": "Categories retrieved successfully"},
    },
    response_model=List[models.Category],
)
async def get_categories():
    """
    Get all categories from the database.

    Returns:
        List[models.Category]: A list of Category objects representing all categories.
    """
    categories = db_categories_driver.find_all()
    return list(categories)


@router.get(
    "/{category_name}",
    summary="Get a category by name",
    description="This endpoint allows you to get a category by name in the database.",
    tags=["categories"],
    responses={
        200: {"description": "Category retrieved successfully"},
        404: {"description": "Category not found"},
    },
    response_model=models.Category,
)
async def get_category(category_name: str):
    """
    Get a category by name from the database.

    Args:
        category_name (str): The name of the category to be retrieved.

    Returns:
        models.Category: A Category object representing the retrieved category.
    """
    if db_categories_driver.count({"name": category_name}) == 0:
        return PlainTextResponse("Category not found", status_code=404)
    category = db_categories_driver.find({"name": category_name})
    return models.Category(**category[0])


@router.get(
    "/{category_name}/sub_categories",
    summary="Get a category's sub categories by name",
    description="This endpoint allows you to get a category's sub categories by name in the database.",
    tags=["categories"],
    responses={
        200: {"description": "Category's sub categories retrieved successfully"},
        404: {"description": "Category not found"},
    },
    response_model=List[str],
)
async def get_category_sub_categories(category_name: str):
    """
    Get a category's sub-categories by name from the database.

    Args:
        category_name (str): The name of the category whose sub-categories are to be retrieved.

    Returns:
        List[str]: A list of strings representing the sub-categories of the retrieved category.
    """
    if db_categories_driver.count({"name": category_name}) == 0:
        return PlainTextResponse("Category not found", status_code=404)
    category = db_categories_driver.find({"name": category_name})
    return models.Category(**category[0]).sub_categories
