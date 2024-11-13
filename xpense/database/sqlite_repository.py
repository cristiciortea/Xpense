import inspect
import sqlite3
from dataclasses import fields
from datetime import datetime
from enum import Enum
from typing import Type, TypeVar, Optional, Any, List, get_origin, get_args, Union

T = TypeVar('T')
DEFAULT_DB_FILE = "xpense.db"


class BaseRepository:
    def __init__(self, model_class: Type[T], db_file: Optional[str] = DEFAULT_DB_FILE):
        """Initialize the repository with a database file."""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Access columns by name.
        self.model_class = model_class

        self.table_name = model_class.__name__.lower() + "s"  # tables are plural.
        self.create_table(self.model_class)

    def create_table(self, model_class: Type[T]):
        """Create a table based on the dataclass fields."""
        columns = []
        for field in fields(model_class):
            column_name = field.name
            column_type = self._get_sqlite_type(field.type)
            if field.name == 'id':
                columns.append(f"{column_name} {column_type} PRIMARY KEY")
            else:
                columns.append(f"{column_name} {column_type}")
        columns_sql = ", ".join(columns)
        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_sql})
        '''
        self.conn.execute(create_table_sql)
        self.conn.commit()

    def add(self, obj: T):
        """Add a new object to the database."""
        column_names = [field.name for field in fields(obj)]
        placeholders = ", ".join("?" for _ in column_names)
        columns_sql = ", ".join(column_names)
        values = [self._serialize_field(getattr(obj, field.name), field.type) for field in fields(obj)]
        insert_sql = f'''
            INSERT INTO {self.table_name} ({columns_sql})
            VALUES ({placeholders})
        '''
        self.conn.execute(insert_sql, values)
        self.conn.commit()

    def get_by_id(self, model_class: Type[T], obj_id: Any) -> Optional[T]:
        """Retrieve an object by its ID."""
        cursor = self.conn.execute(f'''
            SELECT * FROM {self.table_name} WHERE id = ?
        ''', (obj_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_object(row, model_class)
        return None

    def get_all(self) -> List[T]:
        """Retrieve all objects of the given model class."""
        cursor = self.conn.execute(f'''SELECT * FROM {self.table_name}''')
        rows = cursor.fetchall()
        return [self._row_to_object(row, self.model_class) for row in rows]

    def update(self, obj: T):
        """Update an existing object."""
        column_names = [field.name for field in fields(obj) if field.name != 'id']
        assignments = ", ".join(f"{name} = ?" for name in column_names)
        values = [self._serialize_field(getattr(obj, name), field.type)
                  for name, field in zip(column_names, fields(obj)[1:])]  # Skip 'id' field
        values.append(obj.id)
        update_sql = f'''
            UPDATE {self.table_name}
            SET {assignments}
            WHERE id = ?
        '''
        self.conn.execute(update_sql, values)
        self.conn.commit()

    def delete(self, model_class: Type[T], obj_id: Any):
        """Delete an object by its ID."""
        self.conn.execute(f'''
            DELETE FROM {self.table_name} WHERE id = ?
        ''', (obj_id,))
        self.conn.commit()

    def _row_to_object(self, row: sqlite3.Row, model_class: Type[T]) -> T:
        """Convert a database row to an object of type T."""
        init_args = {}
        for field in fields(model_class):
            value = row[field.name]
            init_args[field.name] = self._deserialize_field(value, field.type)
        return model_class(**init_args)

    def _get_sqlite_type(self, py_type: Any) -> str:
        """Map Python types to SQLite types."""
        origin_type = getattr(py_type, '__origin__', None)
        if origin_type is Optional:
            args = getattr(py_type, '__args__', [])
            if args:
                py_type = args[0]
        if py_type in (int, 'int'):
            return 'INTEGER'
        elif py_type in (float, 'float'):
            return 'REAL'
        elif py_type in (str, 'str'):
            return 'TEXT'
        elif py_type in (bool, 'bool'):
            return 'INTEGER'  # SQLite does not have a separate BOOLEAN type
        elif isinstance(py_type, Enum):
            return 'TEXT'
        elif py_type is datetime:
            return 'TEXT'
        else:
            return 'TEXT'  # Default to TEXT for any other types

    def _serialize_field(self, value: Any, field_type: Any) -> Any:
        """Serialize a field value before storing it in the database."""
        if isinstance(value, Enum):
            return value.value
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, bool):
            return int(value)
        else:
            return value

    def _deserialize_field(self, value: Any, field_type: Any) -> Any:
        """Deserialize a field value when retrieving it from the database."""
        if value is None:
            return None
        origin_type = getattr(field_type, '__origin__', None)
        actual_type = field_type

        if get_origin(actual_type) == Union:
            actual_type = get_args(actual_type)[0]

        if inspect.isclass(actual_type) and issubclass(actual_type, Enum):
            return actual_type(value)
        elif actual_type is datetime:
            return datetime.fromisoformat(value)
        elif actual_type is bool:
            return bool(value)
        elif actual_type is int:
            return int(value)
        elif actual_type is float:
            return float(value)
        elif actual_type is str:
            return value
        else:
            return value

    def close(self):
        """Close the database connection."""
        self.conn.close()
