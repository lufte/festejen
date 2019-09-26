1. Instalar dependencias: `pip3 install -r requirements.txt`.
2. Crear la base: `sqlite3 -init db.sql festejen.db ""`.
3. Descargar comentarios de elpais.com.uy: `cd scraper && scrapy crawl elpais`.
   Se puede interrumpir con CTRL-C para descargar unos pocos.
4. Generar un índice con los comentarios descargados: `cd .. && python3 -m
   parser.index`
5. Generar un comentario: `python3 -m parser.generator`.
