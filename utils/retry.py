import time


MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


def retry_operation(operation, operation_name="Operation"):
    """
    Run an operation with limited retries.

    Total attempts = 3
    Retry delays = 2s, 4s
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            return operation()

        except Exception as e:

            if attempt == MAX_RETRIES:

                print(
                    f"\n❌ {operation_name} failed "
                    f"after {MAX_RETRIES} attempts."
                )

                raise e

            delay = INITIAL_RETRY_DELAY * (2 ** (attempt - 1))

            print(
                f"\n⚠️ {operation_name} failed."
            )

            print(
                f"Retrying in {delay} seconds..."
                f" (Attempt {attempt + 1}/{MAX_RETRIES})"
            )

            time.sleep(delay)