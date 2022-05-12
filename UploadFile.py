import os

from constants import (
    ALLOWED_EXTENSIONS,
    UPLOAD_FOLDER
)


#  Upload File class
class UploadFile:
    def __init__(self, filename, secure):
        #  Declares self.variables that can be used
        self.file = filename
        self.secure = secure
        self.path = None
        self.exception = None
        self.fullpath = None

    #  Does the checks before saving file
    def use_file(self):
        if not self.file_checks():
            return self.exception

        self.check_folder()

        if self.exception is None:
            self.save()

    #  Checks if there is a file
    def file_checks(self):
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if self.file.filename == '':
            self.exception = "No selected file"
            return self.exception
        return True

    #  Checks if the file has the right extension (.wav)
    def file_allowed(self):
        return '.' in self.file.filename and \
               self.file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def check_folder(self):
        #  Checks if there is a folder called "Audio"
        #  if not then a folder is created
        self.path = os.getcwd() + "\\" + UPLOAD_FOLDER
        if not os.path.isdir(self.path):
            os.mkdir(UPLOAD_FOLDER)

    def save(self):
        #  Checks if self.file is in existence and file_allowed() is true
        if self.file and self.file_allowed():
            #  Self.secure is used because it is from secure_filename
            #  this is an ASCII string to stop malicious files
            filename = self.secure
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            #  Checks if the file already exists before saving
            if os.path.isfile(filepath):
                self.exception = "File already exists..."
                return self.exception
            #  Saves file
            self.file.save(filepath)
            return filepath
        else:
            self.exception = "This is a file with a wrong extension :("
            return self.exception


