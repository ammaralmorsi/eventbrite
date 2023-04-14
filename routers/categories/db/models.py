from pydantic import BaseModel


class Category(BaseModel):
    """
    A Pydantic model representing a category.

    Attributes:
        name (str): The name of the category.
        sub_categories (List[str]): The list of sub-categories under the category.
    """

    name: str
    sub_categories: list[str] = []

    class Config:
        """
        Configuration class for the Category model.

        Attributes:
            schema_extra (dict): Extra schema information for generating OpenAPI documentation.
            orm_mode (bool): Enables ORM mode to allow using the model with databases.
        """

        schema_extra = {
            "example": {
                "name": "Sports & Fitness",
                "sub_categories": [
                    "Football",
                    "Basketball",
                    "Tennis",
                    "Exercise",
                    "Cycling",
                    "Soccer",
                    "Running",
                    "Golf",
                    "Walking",
                    "Fighting & Martial Arts",
                    "Swimming & Water Sports",
                    "Wrestling",
                    "Baseball",
                    "Mountain Biking",
                    "Camps",
                ]
            }
        }
        orm_mode = True
