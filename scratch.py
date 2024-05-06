from pydantic import BaseModel

class SQLQuery(BaseModel):
    sql_query: str

print(SQLQuery.model_json_schema())