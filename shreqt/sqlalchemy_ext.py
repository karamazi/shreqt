from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement


class CreateView(Executable, ClauseElement):
    def __init__(self, name, select):
        self.name = name
        self.select = select


@compiles(CreateView)
def create_view(element, compiler, **kw):
    view_sql = compiler.process(element.select, literal_binds=True)
    return f"CREATE VIEW {element.name} AS \n{view_sql}"


class DropView(Executable, ClauseElement):
    def __init__(self, name):
        self.name = name


@compiles(DropView)
def drop_view(element, compiler, **kw):
    return f"DROP VIEW {element.name}"
