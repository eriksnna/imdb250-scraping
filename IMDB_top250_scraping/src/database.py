import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Movie, Series

Base = declarative_base()

class MovieDB(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = Column(String)
    rating = Column(String)

class SeriesDB(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = Column(String)
    seasons = Column(Integer)
    episodes = Column(Integer)

def inicializar_banco(db_url):
    if db_url.startswith("sqlite:///"):
        caminho_arquivo = db_url.replace("sqlite:///", "")
        
        diretorio = os.path.dirname(caminho_arquivo)
        
        if diretorio and not os.path.exists(diretorio):
            try:
                os.makedirs(diretorio)
                print(f"diretório do banco criado: {diretorio}")
            except OSError as e:
                print(f"erro ao criar diretório do banco: {e}")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

def salvar_catalogo(engine, catalogo):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    contador = 0
    print("salvando no banco de dados...")
    
    for item in catalogo:
        entry = None
        
        if isinstance(item, Movie):
            entry = MovieDB(title=item.title, year=item.year, rating=item.rating)
        elif isinstance(item, Series):
            entry = SeriesDB(title=item.title, year=item.year, seasons=item.seasons, episodes=item.episodes)
            
        if entry:
            try:
                session.add(entry)
                session.commit()
                contador += 1
            except IntegrityError:
                session.rollback()
                
    print(f"novos registros salvos: {contador}")
    session.close()