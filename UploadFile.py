import os

from constants import (
    ALLOWED_EXTENSIONS,
    UPLOAD_FOLDER
)


class UploadFile:
    def __init__(self, filename, secure):
        self.file = filename
        self.secure = secure
        self.path = None
        self.exception = None
        self.fullpath = None

    def use_file(self):
        if not self.file_checks():
            return self.exception

        self.check_folder()

        if self.exception is None:
            self.save()

    def file_checks(self):
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if self.file.filename == '':
            self.exception = "No selected file"
            return self.exception

        return True

    def file_allowed(self):
        return '.' in self.file.filename and \
           self.file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def check_folder(self):
        #  Checks if there is a folder called "Audio"
        #  if not then a folder is created
        self.path = os.getcwd() + "\Audio"
        if not os.path.isdir(self.path):
            os.mkdir("Audio")

    def save(self):
        if self.file and self.file_allowed():
            filename = self.secure
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            self.file.save(filepath)
            self.fullpath = filepath
            return filepath
        else:
            self.exception = "This is a file with a wrong extension :("
            return self.exception

    def getFilepath(self):
        return self.fullpath


