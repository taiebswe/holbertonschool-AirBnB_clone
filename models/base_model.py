from datetime import datetime
from models import storage
import uuid

class BaseModel:
    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if "__class__" != k:
                    if k in ("created_at", "updated_at"):
                        setattr(self, k, datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, k, v)
            return
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        storage.new(self)
    
    def __str__(self):
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")
        
    def save(self):
        self.updated_at = datetime.now()
        storage.save()
        
    def to_dict(self):
        self.__dict__['__class__'] = self.__class__.__name__
        self.__dict__['created_at'] = self.created_at.isoformat()
        self.__dict__['updated_at'] = self.updated_at.isoformat()
        return self.__dict__