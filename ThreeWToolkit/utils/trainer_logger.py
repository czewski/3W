from abc import ABC
import os
import json
import pickle
from datetime import datetime

class TrainerLogger(ABC):
    pass

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
        # Validate file format
        if file_format not in ["json", "pickle"]:
            raise ValueError(
                "file_format must be either 'json' or 'pickle'"
            )

        # Create directory if it does not exist
        os.makedirs(log_dir, exist_ok=True)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = ".json" if file_format == "json" else ".pkl"
        filename = f"log_{timestamp}{extension}"
        file_path = os.path.join(log_dir, filename)

        # Save log file
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

            print(f"[TrainerLogger] Log saved at: {file_path}")
        except Exception as e:
            print(
                f"[TrainerLogger] Failed to save optimization progress: {e}"
            )
            raise

        return file_path