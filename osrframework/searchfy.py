#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
##################################################################################
#
#    Copyright 2015 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This program is part of OSRFramework. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

''' 
searchfy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2015
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions. For additional info, visit to <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
__author__ = "Felix Brezo, Yaiza Rubio "
__copyright__ = "Copyright 2015, i3visio"
__credits__ = ["Felix Brezo", "Yaiza Rubio"]
__license__ = "GPLv3+"
__version__ = "v0.6.0"
__maintainer__ = "Felix Brezo, Yaiza Rubio"
__email__ = "contacto@i3visio.com"


import argparse
import json
import os

import osrframework.utils.platform_selection as platform_selection
import osrframework.utils.general as general

def performSearch(platformNames=[], queries=[], process=False):
    ''' 
        Method to perform the phone list.
        
        :param platforms: List of <Platform> objects.
        :param queries: List of queries to be performed.
        :param process: Whether to process all the profiles... SLOW!
        
        :return:
    '''
    # Grabbing the <Platform> objects
    platforms = platform_selection.getPlatformsByName(platformNames, mode="searchfy")    
    
    results = []
    for q in queries:
        for pla in platforms:
            # This returns a json.txt!
            entities = pla.getInfo(query=q, process = process, mode="searchfy")
            if entities != "[]":
                results += json.loads(entities)
    return results

def searchfy_main(args):
    ''' 
        Main program.
        
        :param args: Arguments received in the command line.
    '''
    results = performSearch(platformNames=args.platforms, queries=args.queries, process = args.process)

    # Generating summary files for each ...
    if args.extension:
        # Storing the file...
        #logger.info("Creating output files as requested.")
        if not args.maltego:
            # Verifying if the outputPath exists
            if not os.path.exists (args.output_folder):
                #logger.warning("The output folder \'" + args.output_folder + "\' does not exist. The system will try to create it.")
                os.makedirs(args.output_folder)
                
        # Grabbing the results 
        fileHeader = os.path.join(args.output_folder, args.file_header)
        
        if not args.maltego:
            # Iterating through the given extensions to print its values
            for ext in args.extension:
                # Generating output files
                general.exportUsufy(results, ext, fileHeader)
                
    # Generating the Maltego output    
    if args.maltego:
        general.listToMaltego(results)

    # Printing the results if requested
    if not args.maltego:
        print "A summary of the results obtained are listed in the following table:"
        print unicode(general.usufyToTextExport(results))
        print "You will find all the information collected in the following files:"                                                     
        for ext in args.extension:
            # Generating output files
            print "\t-" + fileHeader + "." + ext
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='searchfy.py - Piece of software that performs a query on the platforms in OSRFramework.', prog='searchfy.py', epilog='Check the README.md file for further details on the usage of this program or follow us on Twitter in <http://twitter.com/i3visio>.', add_help=False)
    parser._optionals.title = "Input options (one required)"

    # Defining the mutually exclusive group for the main options
    groupMain = parser.add_mutually_exclusive_group(required=True)
    # Adding the main options
    groupMain.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3+ license and exists.')    
    groupMain.add_argument('-q', '--queries', metavar='<searches>', nargs='+', action='store', help = 'the list of queries to be performed).')

    listAll = platform_selection.getAllPlatformNames("searchfy")

    # Configuring the processing options
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the way in which searchfy will process the identified profiles.')
    #groupProcessing.add_argument('-L', '--logfolder', metavar='<path_to_log_folder', required=False, default = './logs', action='store', help='path to the log folder. If none was provided, ./logs is assumed.')        
    # Getting a sample header for the output files

    groupProcessing.add_argument('-e', '--extension', metavar='<sum_ext>', nargs='+', choices=['csv', 'json', 'mtz', 'ods', 'txt', 'xls', 'xlsx' ], required=False, default = ['ods'], action='store', help='output extension for the summary files. Default: ods.')    
    groupProcessing.add_argument('-F', '--file_header', metavar='<alternative_header_file>', required=False, default = "profiles", action='store', help='Header for the output filenames to be generated. If None was provided the following will be used: profiles.<extension>' )          
    groupProcessing.add_argument('-m', '--maltego', required=False, action='store_true', help='Parameter specified to let usufy.py know that he has been launched by a Maltego Transform.')    
    groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', required=False, default = './results', action='store', help='output folder for the generated documents. While if the paths does not exist, usufy.py will try to create; if this argument is not provided, usufy will NOT write any down any data. Check permissions if something goes wrong.')
    groupProcessing.add_argument('-p', '--platforms', metavar='<platform>', choices=listAll, nargs='+', required=False, default =['all'] ,action='store', help='select the platforms where you want to perform the search amongst the following: ' + str(listAll) + '. More than one option can be selected.')    
    groupProcessing.add_argument('--process', required=False, default =False ,action='store_true', help='whether to process the info in the profiles recovered. NOTE: this would be much slower.')    
        
    # About options
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    #groupAbout.add_argument('-v', '--verbose', metavar='<verbosity>', choices=[0, 1, 2], required=False, action='store', default=1, help='select the verbosity level: 0 - none; 1 - normal (default); 2 - debug.', type=int)
    groupAbout.add_argument('--version', action='version', version='%(prog)s ' +__version__, help='shows the version of the program and exists.')

    args = parser.parse_args()    

    # Calling the main function
    searchfy_main(args)
