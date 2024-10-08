from src.logger import setup_logger

logger = setup_logger('example', 'logs/example.log')

def add_numbers(a, b):
    logger.info(f"Adding numbers: {a} + {b}")
    result = a + b
    logger.info(f"Result: {result}")
    return result

# Exemple d'utilisation
if __name__ == "__main__":
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")