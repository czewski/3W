from abc import ABC
import os
import json
import pickle
import logging
from datetime import datetime

class TrainerLogger(ABC):

    @staticmethod
    def log_optimization_progress(
        progress_log: dict,
        log_dir: str = "logs",
        file_format: str = "json"
    ) -> str:
        """
        Logs the optimization progress to a JSON or Pickle file.

        Args:
            progress_log (dict): Dictionary containing optimization results.
            log_dir (str): Directory where the log file will be saved.
            file_format (str): Format of the file: 'json' or 'pickle'.

        Returns:
            str: Path to the saved log file.
        """

        logger = logging.getLogger("TrainerLogger")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        if file_format not in ["json", "pickle"]:
            raise ValueError(
                "file_format must be either 'json' or 'pickle'"
            )

        if not isinstance(progress_log, dict):
            raise TypeError(
                "progress_log must be a dictionary"
            )
        
        if not progress_log:
            raise ValueError(
                "progress_log must be a non-empty dictionary"
            )

        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = ".json" if file_format == "json" else ".pkl"
        filename = f"log_{timestamp}{extension}"
        file_path = os.path.join(log_dir, filename)

        try:
            if file_format == "json":
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(
                        progress_log,
                        f,
                        ensure_ascii=False,
                        indent=4
                    )
            else:
                with open(file_path, 'wb') as f:
                    pickle.dump(progress_log, f)

            logger.info("Log saved at: %s", file_path)
        except Exception as e:
            logger.error("Failed to save optimization progress: %s", e)
            raise

        return file_path