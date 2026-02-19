from datetime import date
from decimal import Decimal
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, PositiveInt, field_validator

T = TypeVar("T")

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

class PaginatedResponse(BaseModel, Generic[T]):  # noqa: D101
    datas: List[T] = Field(description="Lista de itens da página atual")
    count: int = Field(ge=0, description="Total de itens disponíveis")
    current_page: PositiveInt = Field(ge=1, description="Página atual")
    per_page: PositiveInt = Field(ge=1, description="Quantidade de itens por pagina")
    total_pages: PositiveInt = Field(description="Quantidade total de pagina")


class VendReport(BaseModel):  # noqa: D101
    c_codvend: Optional[str] = Field(None, description="Código do vendedor")
    c_codigo: Optional[str] = Field(None, description="Código do cliente")
    c_cliente: Optional[str] = Field(None, description="Nome do cliente")
    c_numero: Optional[str] = Field(None, description="Número do pedido")
    data_pedido: Optional[date] = Field(None, description="Data do pedido")
    c_ntfiscal: Optional[str] = Field(None, description="Número da nota fiscal")
    data_movimento: Optional[date] = Field(None, description="Data do movimento")
    cod_produto: Optional[str] = Field(None, description="Código do produto")
    desc_produto: Optional[str] = Field(None, description="Descrição do produto")
    c_prcusto: Optional[Decimal] = Field(None, description="Custo do produto")
    c_preco: Optional[Decimal] = Field(None, description="Preço do produto")
    margem_valor: Optional[Decimal] = Field(None, description="Margem em valor")
    margem_porcentagem: Optional[Decimal] = Field(
        None, description="Margem em porcentagem"
    )
    c_valor: Optional[Decimal] = Field(None, description="Valor de pagamento")
    data_pagamento: Optional[date] = Field(None, description="Data do pagamento")
    total_nota: Optional[Decimal] = Field(None, description="Total da nota")
    media_margem_porcent_vendedor: Optional[Decimal] = Field(
        None, description="Média da margem em porcentagem por vendedor"
    )
    valor_2_5_porcento: Optional[Decimal] = Field(
        None, description="2,5 % do valor de pagamento"
    )

    @field_validator(
        "c_codvend",
        "c_codigo",
        "c_cliente",
        "c_numero",
        "c_ntfiscal",
        "cod_produto",
        "desc_produto",
        mode="after",
    )
    @classmethod
    def strip_fields(cls, value: str) -> str:  # noqa: D102
        return value.strip()

    @field_validator(
        "c_prcusto",
        "c_preco",
        "margem_valor",
        "margem_porcentagem",
        "c_valor",
        "total_nota",
        "media_margem_porcent_vendedor",
        "valor_2_5_porcento",
        mode="before",
    )
    @classmethod
    def none_to_decimal(cls, value) -> Decimal:  # noqa: D102
        if value is None:
            return Decimal("0.00")
        return value
