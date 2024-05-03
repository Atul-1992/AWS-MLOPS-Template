import os
from functools import wraps

import hydra
from hydra import TaskFunction
from omegaconf import DictConfig


class Utils:
    @classmethod
    def text_appender(cls, root, text):
        path = os.path.join(root, text)
        # Check if .gitignore file exists
        if not os.path.exists(path):
            cls.file_writer_add_text(path, text, "w")
        else:
            # Append directory pattern to .gitignore file
            cls.file_writer_add_text(path, text, "a")

    @classmethod
    def file_writer_add_text(cls, file, text, method):
        if method not in ["w", "a"]:
            return False
        mode = "w" if method == "w" else "a"
        try:
            with open(file, mode, encoding="utf-8") as f:
                if text + "\n" in f.read_lines():
                    return True
                f.write(f"{text}\n")
            return True
        except IOError:
            return False


def config_initializer(script_path):

    def decorator(taskfunction: TaskFunction):
        rel_path = os.path.relpath("./configs", os.path.dirname(script_path))

        @hydra.main(config_name="config", config_path=(rel_path), version_base=None)
        @wraps(taskfunction)
        def decorated_main(cfg: DictConfig):
            return taskfunction(cfg)

        return decorated_main

    return decorator
