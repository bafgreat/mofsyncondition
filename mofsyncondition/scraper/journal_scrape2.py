#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import os
# import re
import glob
import concurrent.futures
from functools import partial
import threading
import numpy as np
from mofsyncondition.io import journal_api
from mofsyncondition.io import filetyper

doi_data = filetyper.load_data('../db/csv/doi.csv')
external_drive_path = os.path.abspath('/Volumes/X9 Pro/MOF_data/doi_html')
all_dois = list(doi_data.DOI)

def uncompleted(all_doi, path_to_folder):
    html_files = sorted(glob.glob(path_to_folder+'/*'))
    all_file_names = [ molfile[:molfile.rindex('.')].split('/')[-1] for molfile in html_files]
    for doi in all_doi:
        outfile = doi.replace("/", "_forward_")
        if outfile not in all_file_names:
            print (doi)
            out_path = external_drive_path+'/'+outfile
            try:
                parallel_downloader(doi, out_path)
            except :
                pass






# def downloader(doi, path_to_out):
#     download_functions = [
#         journal_api.download_from_springer,
#         journal_api.download_from_elsevier,
#         journal_api.download_from_wiley,
#         journal_api.download_from_rsc,
#         journal_api.download_from_acs,
#         journal_api.download_from_acs,
#         journal_api.download_from_taylor_and_francis
#     ]
#     value = False
#     for download_function in download_functions:
#         try:
#             value = download_function(doi, path_to_out)
#         except:
#             pass
#         if value is True:
#             return value

#     return value


# def downloader(doi, path_to_out, download_function):
#     try:
#         return download_function(doi, path_to_out)
#     except Exception as e:
#         # Handle exceptions if needed
#         print(f"Error downloading using {download_function.__name__}: {e}")
#         return False


# def parallel_downloader(doi, path_to_out):
#     download_functions = [
#         journal_api.download_from_springer,
#         journal_api.download_from_elsevier,
#         journal_api.download_from_wiley,
#         journal_api.download_from_rsc,
#         journal_api.download_from_acs,
#         journal_api.download_from_acs,
#         journal_api.download_from_taylor_and_francis
#     ]

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         # Use partial to create a function with fixed arguments (doi, path_to_out)
#         partial_downloader = partial(downloader, doi, path_to_out)

#         # Submit tasks to the executor
#         futures = [executor.submit(partial_downloader, func)
#                    for func in download_functions]

#         # Wait for all tasks to complete
#         concurrent.futures.wait(futures)

#         # Get results from completed tasks
#         results = [future.result() for future in futures]

#     # Check if any download succeeded
#     return any(results)
# def downloader(doi, path_to_out, download_function, event, result_list):
#     try:
#         result = download_function(doi, path_to_out)
#         if result:
#             result_list.append(result)
#             event.set()  # Set the event to signal other threads to stop
#     except Exception as e:
#         # Handle exceptions if needed
#         print(f"Error downloading using {download_function.__name__}: {e}")

# def parallel_downloader(doi, path_to_out):
#     download_functions = [
#         journal_api.download_from_springer,
#         journal_api.download_from_elsevier,
#         journal_api.download_from_wiley,
#         journal_api.download_from_rsc,
#         journal_api.download_from_acs,
#         journal_api.download_from_acs,
#         journal_api.download_from_taylor_and_francis
#     ]

#     # Create an event to signal other threads to stop
#     stop_event = threading.Event()

#     # Create an empty list to store results
#     result_list = []

#     # Create and start threads
#     threads = []
#     for func in download_functions:
#         thread = threading.Thread(target=downloader, args=(doi, path_to_out, func, stop_event, result_list))
#         threads.append(thread)
#         thread.start()

#     # Wait for any thread to finish or all threads to finish
#     stop_event.wait()

#     # Stop remaining threads
#     for thread in threads:
#         thread.join()

#     # Return True if any download succeeded
#     return any(result_list)

def downloader(doi, path_to_out, download_function):
    try:
        return download_function(doi, path_to_out)
    except Exception as e:
        # Handle specific exceptions if needed
        print(f"Error downloading using {download_function.__name__}: {e}")
        return False

def parallel_downloader(doi, path_to_out):
    download_functions = [
        journal_api.download_from_springer,
        journal_api.download_from_elsevier,
        journal_api.download_from_wiley,
        journal_api.download_from_rsc,
        journal_api.download_from_acs,
        journal_api.download_from_acs,
        journal_api.download_from_taylor_and_francis
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use partial to create a function with fixed arguments (doi, path_to_out)
        partial_downloader = partial(downloader, doi, path_to_out)

        # Submit tasks to the executor
        futures = [executor.submit(partial_downloader, func) for func in download_functions]

        # Wait for any thread to finish or all threads to finish
        concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

        # Cancel remaining tasks
        for future in futures:
            future.cancel()

        # Get results from completed tasks
        results = [future.result() for future in futures if future.done()]


    # Check if any download succeeded
    print ("Result", results)
    return any(results)


uncompleted(all_dois, external_drive_path)