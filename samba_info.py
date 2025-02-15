import os
import time
import logging
from smb.SMBConnection import SMBConnection

# Set up logging
logging.basicConfig(filename='samba_info.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_samba_info():
    try:
        # Connect to Samba Share
        conn = SMBConnection(username='your_username', password='your_password',
                              client_name='client_name', server_name='server_name',
                              domain='', use_ntlm_v2=True)
        conn.connect('server_ip', 139)  # or port 445

        # Get disk space information
        free_space = conn.getDiskFreeSpace('shared_folder')

        # List files and filter by size
        files = []
        for filename in conn.listPath('shared_folder', '/'):
            if filename.isDirectory:
                continue
            file_size = conn.getAttributes('shared_folder', filename.filename).file_size
            if file_size > 100 * 1024 * 1024:  # Filter files > 100MB (example)
                files.append((filename.filename, file_size))

        conn.close()

        # Log the successful data retrieval
        logging.info("Successfully retrieved Samba share information.")

        return free_space, files, time.strftime('%Y-%m-%d %H:%M:%S')
    
    except Exception as e:
        # Log any errors
        logging.error(f"Error retrieving Samba share information: {e}")
        return None, None, None

def update_data():
    # Fetch updated data
    free_space, files, last_updated = get_samba_info()
    
    if free_space is None:
        return {'error': 'Failed to retrieve data from Samba share'}

    # Log the update call
    logging.info("Data update requested.")

    # Return the data to be sent to the frontend
    return {'free_space': free_space, 'files': files, 'last_updated': last_updated}
