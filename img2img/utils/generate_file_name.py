import os
import tempfile


def generate_name_file(filename):
    _, ext = os.path.splitext(filename)
    random_filename = tempfile.NamedTemporaryFile(delete=True).name + ext
    random_filename = os.path.basename(random_filename)
    return random_filename
