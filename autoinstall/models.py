from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from .database import Base
from typing import List


class InstallFile(Base):
    __tablename__ = 'install_file'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(254), index=True, unique=True)
    md5 = Column(String(1024), index=True, unique=True)
    install_tree_map: Mapped[List["InstallTreeLinkFile"]] = relationship(back_populates="file_map")


class InstallFilePath(Base):
    __tablename__ = 'install_file_path'
    id = Column(Integer, primary_key=True)
    path = Column(String(1024), index=True)
    file_id = Column(Integer, ForeignKey('install_file.id'), index=True)
    file = relationship("InstallFile", back_populates="pathes")


InstallFile.pathes = relationship("InstallFilePath", back_populates = "file")


class ScanFolder(Base):
    __tablename__ = 'scan_folder'
    id = Column(Integer, primary_key=True)
    path = Column(String(1024))


class InstallTree(Base):
    __tablename__ = 'install_tree'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(128))
    parent_id = Column(Integer, ForeignKey('install_tree.id'), nullable=True)
    install_file_map: Mapped[List["InstallTreeLinkFile"]] = relationship(back_populates="tree_map")


class InstallTreeLinkFile(Base):
    __tablename__ = 'install_tree_link_file'
    tree_id: Mapped[int] = mapped_column(ForeignKey('install_tree.id'), primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey('install_file.id'), unique=True)
    tree_map: Mapped["InstallTree"] = relationship(back_populates="install_file_map")
    file_map: Mapped["InstallFile"] = relationship(back_populates="install_tree_map")