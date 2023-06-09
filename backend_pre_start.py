import os
import json

import logging
import logging.config
import os
from os import path
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.db.session import SessionLocal

# Config logging
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
credentials = os.environ["FIREBASE_CREDENTIALS"]

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")

        # Create File Json FireBase
        if not os.path.isfile(path):
            firebaseCredentials = json.loads(credentials)
            with open(path, "w") as outfile:
                json.dump(firebaseCredentials, outfile)

    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
