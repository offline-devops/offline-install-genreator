from pydantic import BaseModel, EmailStr
from typing import List


class ScanFolderAdd(BaseModel):
    path: str


class ScanFolder(BaseModel):
    path: str
    id: int

    class Config:
        orm_mode = True


class InstallFilePath(BaseModel):
    path: str

    class Config:
        orm_mode = True


class InstallFileUpdate(BaseModel):
    name: str
    path: List[InstallFilePath]

    class Config:
        orm_mode = True


class InstallFile(BaseModel):
    name: str
    id: int
    pathes: List[InstallFilePath]

    class Config:
        orm_mode = True


