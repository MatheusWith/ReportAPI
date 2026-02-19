from datetime import date

from pydantic import BaseModel, Field, PositiveInt


class PaginationParams(BaseModel):  # noqa: D101
    current_page: PositiveInt = Field(1, description="Número da página (começa em 1)")
    per_page: PositiveInt = Field(
        20, ge=1, le=100, description="Quantidade de itens por página"
    )

    @property
    def offset(self) -> int:  # noqa: ANN201
        return (self.current_page - 1) * self.per_page

class VendParams(PaginationParams):  # noqa: D101
    start_date: date
    end_date: date
