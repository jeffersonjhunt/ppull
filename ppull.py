# Copyright 2019 Jefferson J. Hunt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import pandas as pd
import re


class EventPuller():

    def get_matches(self, event_id, filename, debug=False):

        regex = r"^stage\s*\d*"
        stages = dict()
        url = 'https://s3.amazonaws.com/ps-scores/production/%s/html/matchCombined' % event_id

        if(debug):
            print "creating Excel file '{}'".format(filename)

        writer = pd.ExcelWriter(filename)

        if(debug):
            print "importing data from '{}'".format(url)

        data = pd.read_html(url)[0] # read the match combined scores
        data.to_excel(writer, sheet_name='Combined')  # create the Excel

        # for each 'stage' construct the combinded url
        for column in data.columns:
            column_name = column[0]
            match = re.search(regex, column_name, re.IGNORECASE)
            if match:
                stage_id = ''.join(column_name.lower().split())
                stage_url = 'https://s3.amazonaws.com/ps-scores/production/%s/html/%sCombined' % (event_id, stage_id)
                stages[column_name] = stage_url
        
        # create a tab for each 'stage' and add it to the Excel
        for stage_name, stage_url in stages.items():
            if(debug):
                print "importing data from '{}'".format(stage_url)
            data = pd.read_html(stage_url)[0]
            data.to_excel(writer, sheet_name=stage_name)

        if(debug):
            print "saving Excel file".format(stage_url)
        writer.save()

def main():
    
    parser = argparse.ArgumentParser(prog='Invoke-ExamInstance') 
    parser.add_argument('--debug', action='store_true', help='debug logging') 
    parser.add_argument('--filename', required=True, help='filename to create, xlsx is added automatically') 
    parser.add_argument('--event_id', required=True, help='event id to pull from practiscore.com') 
    
    args = parser.parse_args() 

    event_puller = EventPuller()
    event_puller.get_matches(args.event_id, '%s.xlsx' % args.filename, args.debug)

if __name__ == "__main__": 
    main()