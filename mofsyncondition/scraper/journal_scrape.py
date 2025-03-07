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

external_drive_path = os.path.abspath('/Volumes/X9 Pro/All_HTML')
doi_data = filetyper.load_data('../db/csv/DIO_2021_and_other_properties.csv')
# refcodes = [d for d in list(doi_data.Refcode)]
all_refcodes = sorted([name[:name.rindex('.')].split(
    '/')[-1] for name in glob.glob('../../../../MOF_structures/data/Valid/*cif')])

doi_data2 = filetyper.load_data('../db/csv/doi.csv')


def index_data(refcode, data):
    if isinstance(data, dict):
        return data[refcode]
    else:
        return data.loc[data['Refcode'] == refcode]


def doi_index(doi, data):
    if isinstance(data, dict):
        return data[doi]
    else:
        return data.loc[data['DOI'] == doi
                        ]


def find_refcode(path_to_file):
    '''
    function to compile doi of undownloaded journals
    '''
    html_files = sorted(f for f in glob.glob(
        path_to_file + '/*') if f.endswith(('html', 'pdf', 'xml')))
    all_html_files = [file_path for file_path in html_files
                      if os.stat(file_path).st_size > 500]
    all_html_refcodes = [i.split('/')[-1].split('.')[0]
                         for i in all_html_files]
    return all_html_refcodes


def find_doi(doi_data, refcode):
    doi_data = doi_data.replace(np.nan, 'ERROR')
    data = index_data(refcode, doi_data)
    doi = data.DOI.values[0]
    return doi


def find_refs(doi_data, doi):
    doi_data = doi_data.replace(np.nan, 'ERROR')
    data = doi_index(doi, doi_data)
    all_refs = data.Refcode.values[0]
    return all_refs

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

def doi_downloader(all_refcodes, doi_data, doi):
    report = {}
    refcodes = find_refs(doi_data, doi)
    if not any(x in all_refcodes for x in refcodes):
        verdict = parallel_downloader(doi, refcodes)
        print(refcodes, doi, verdict)
        report['verdict'] = verdict
        report['refcodes'] = refcodes
        # report['doi'] = doi
        return report
    else:
        return report


def download_paper_from_doi(all_refcodes, path_to_file, doi_data):
    downloaded_html_refcodes = find_refcode(path_to_file)
    for refcode in all_refcodes:
        if refcode not in downloaded_html_refcodes:
            doi = find_doi(doi_data, refcode)
            if doi != 'ERROR':
                path_to_out = path_to_file+'/'+refcode+'.html'
                verdict = parallel_downloader(doi, refcode)
                print(refcode, doi, verdict)


def csd_doi_paper_downloader(all_refcodes, doi_data, seen_doi, failed_doi, path_to_file):
    done = {}
    data = doi_data.replace(np.nan, 'ERROR')
    all_dois = [i for i in data.DOI.values if i != 'ERROR']
    downloaded_html_refcodes = find_refcode(path_to_file)
    all_refcodes = [
        i for i in all_refcodes if not i in downloaded_html_refcodes]
    #for doi in all_dois:
    for doi in ["10.1039/C5CE02277K"]:
        if doi not in seen_doi:
            report = doi_downloader(all_refcodes, doi_data, doi)
            if report['verdict'] is False:
                failed_doi[doi] = report
                filetyper.append_json(failed_doi, 'failed_doi.json')

        seen_doi.append(doi)
        done['seen'] = seen_doi
        filetyper.append_json(done, 'seen_doi.json')


seen_doi = sorted(filetyper.load_data('seen_doi.json')['seen'])
failed_doi = filetyper.load_data('failed_doi.json')


csd_doi_paper_downloader(all_refcodes, doi_data2,
                         seen_doi, failed_doi, external_drive_path)
# print (find_refs(doi_data2, '10.7868/S0132344X14060024'))
# check_similar_doi(all_refcodes, doi_data2, '10.7868/S0132344X14060024')
# download_paper_from_doi(all_refcodes, external_drive_path, doi_data)
# check_similar_doi(all_refcodes, doi_data2)
