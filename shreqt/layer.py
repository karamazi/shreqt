from typing import Optional, List, Type
from shreqt.model import ModelBase, ViewBase, full_table_name


class Layer:
    def __init__(
        self,
        *,
        schemas: Optional[List[str]] = None,
        tables: Optional[List[Type[ModelBase]]] = None,
        views: Optional[List[Type[ViewBase]]] = None,
        models: Optional[List[ModelBase]] = None,
    ):
        self.tables = tables or []
        self.schemas = schemas or []
        self.models = models or []
        self.views = views or []

    def to_list_push(self):
        return self.schemas + self.tables + self.views + self.models

    def to_list_pop(self):
        return self.models + self.views + self.tables + self.schemas


class LayerBuilder:
    def __init__(self):
        self.tables = {}
        self.schemas = []
        self.models = []
        self.views = []

    def with_table(self, table: Type[ModelBase]):
        full_name = full_table_name(table)
        self.tables[full_name] = table
        return self

    def with_tables(self, *tables: Type[ModelBase]):
        for table in tables:
            self.with_table(table)
        return self

    def with_schema(self, schema: str):
        self.schemas.append(schema)
        return self

    def with_schemas(self, *schemas: str):
        for schema in schemas:
            self.with_schema(schema)
        return self

    def with_view(self, view: Type[ViewBase]):
        self.views.append(view)
        return self

    def with_views(self, *views: Type[ViewBase]):
        for view in views:
            self.with_view(view)
        return self

    def with_model(self, model: ModelBase):
        self.models.append(model)
        return self

    def with_models(self, *models: ModelBase):
        for model in models:
            self.with_model(model)
        return self

    def build(self):
        return Layer(
            schemas=self.schemas,
            tables=list(self.tables.values()),
            models=self.models,
            views=self.views,
        )
