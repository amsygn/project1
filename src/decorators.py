def log(filename=None):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                # Логируем успешное завершение функции
                ok_message = f"{func.__name__} ok\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(ok_message)
                else:
                    print(ok_message, end="\n")
                return result
            except Exception as e:
                # Логируем ошибку
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, kwargs: {kwargs}\n"
                )
                if filename:
                    with open(filename, "a") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="\n")
                return None

        return wrapper
    return my_decorator
