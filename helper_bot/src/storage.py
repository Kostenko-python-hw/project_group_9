import os
import sys

package_path = os.path.dirname(os.path.abspath(sys.argv[0]))
NOTES_FILE_NAME = os.path.join(package_path, r'notes_data.bin')
CONTACTS_FILE_NAME = os.path.join(package_path, r'storage.bin')
