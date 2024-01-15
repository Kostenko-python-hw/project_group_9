import os
import sys

package_path = os.path.dirname(sys.modules['__main__'].__file__)
NOTES_FILE_NAME = os.path.join(package_path, 'notes_data.bin')
CONTACTS_FILE_NAME = os.path.join(package_path, 'storage.bin')
