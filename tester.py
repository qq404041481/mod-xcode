from pbxproj import XcodeProject
from pbxproj.pbxextensions import *


'''
Useful methods:
project.get_file_by_id
project.get_files_by_name
project.get_files_by_path

project.get_groups_by_name
project.get_groups_by_path

project.get_object(id)

object.get_id()
'''

config = {
'xcodeproj': './cloud-search.xcodeproj'
}
# open project
project = XcodeProject.load(config['xcodeproj'] + '/project.pbxproj')

class GroupStruct:
    Dict = {} # if an object has parrent, then it's content is it's parent
    def __init__(self, project):
        self.groups = project.objects.get_objects_in_section('PBXGroup')

        # initialize the dictionary of groups
        for item in self.groups:
            itemID = item.get_id().upper()
            for child in item.children:
                self.Dict[child.upper()] = itemID

    '''
        input: file id
        output: None if over maxIter, list of groups
    '''
    def iterateFiles(self, fileID, maxIter = 100):
        curr = fileID
        list = []
        iter = 0
        while curr in self.Dict:
            parent = self.Dict[curr]
            list.append(parent)
            curr = parent
            iter += 1
            if iter > maxIter:
                return None

        return list

    def constructPath(self):
        pass

'''
Add exisiting file to header.
1. Find the file ID in PBXFileReference. 
2. Add entry in PBXBuildFile (Check if exist) with correct settings (public/private/project)
3. Find correct PBXHeadersBuildPhase section. Add PBXBuildFile to files

1. Find the exisiting file. with project.get_files_by_name
2. 

project.get_build_files_for_file(file.get_id()) get the targets with the file
input:
    project: xcode file
    fileObj: file object, get through get_files or get_file
    headerScope: scope of headers (PROJECT/PRIVATE/PUBLIC)
    targetName: which target to add to
    force: True to override options (reduce to only one), false to allow add multiple instances.
'''
def addExistingFileToHeader(project, fileObj, headerScope = HeaderScope.PUBLIC, targetName=None, force=True):
    fileRef = fileObj # check for fileref
    fileOptions = FileOptions(header_scope=headerScope)
    file_type, expected_build_phase = ProjectFiles._determine_file_type(fileRef, fileOptions.ignore_unknown_type)
    print(expected_build_phase)
    buildFile = project._create_build_files(fileRef, targetName, expected_build_phase, fileOptions)

    return buildFile

if __name__ == '__main__':
    test = GroupStruct(project)
    a = addExistingFileToHeader(project, project.get_files_by_name('AAPLAppDelegate.h')[0], targetName = 'CloudSearch')
    print(a)
    project.save()