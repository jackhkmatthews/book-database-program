import logging

logging.basicConfig(
    force=True,
    filename="book-database-program.log",
    encoding="utf-8",
    level=logging.DEBUG,
)

logger = logging.getLogger("book-database-program")
