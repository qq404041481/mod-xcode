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
phaseType: PBXResourcesBuildPhase. Resources/Headers/Sources/Frameworks
targetName: 'string'
'''
def getPhaseInTarget(project, phaseType, targetObj):
    for phase in targetObj.buildPhases:
        if isinstance(project.get_object(phase), phaseType):
            return phase

    return None

'''
targetName: specific target object
fileObjs: can be more than one 


'''
def checkHeader(project, fileObjs, targetObj = None):
    PBXHeadersBuildPhaseList = []

    for fileObj in fileObjs:
        fileID = fileObj.get_id()
        if targetObj:
            phaseID = getPhaseInTarget(project, PBXHeadersBuildPhase, targetObj)
            phase = project.get_object(phaseID)
            for phaseFile in phase.files:
                if phaseFile == fileObj.get_id():
                    return fileObj


    return None

def checkAllHeaders():
    TargetList = project.objects.get_targets()


'''
Add exisiting file (valid fileRef) to header.
1. Find the file ID in PBXFileReference. 
2. Add entry in PBXBuildFile (Check if exist) with correct settings (public/private/project)
3. Find correct PBXHeadersBuildPhase section. Add PBXBuildFile to files

1. Find the exisiting file. with project.get_files_by_name
2. project.get_build_files_for_file(fileId)
3. get Buildfile ID
4. Find target, project.get_target_by_name('target')
5. Find target Header using project.get_target_by_name('target').buildPhases (loop through, use type(get_object()) check for PBXHeadersBuildPhase)
6. Get header phase, check for the Buildfile ID

project.get_build_files_for_file(file.get_id()) get the targets with the file
input:
    project: xcode file
    fileObj: file object, get through get_files or get_file
    headerScope: scope of headers (PROJECT/PRIVATE/PUBLIC)
    targetName: which target to add to
    force: True to override options (reduce to only one), false to allow add multiple instances. !!! should be True !!!
'''
def addExistingFileToHeader(project, fileObj, targetName, headerScope = HeaderScope.PRIVATE, force=True):
    buildfiles = project.get_build_files_for_file(fileObj.get_id())  # can have multiple BuildFiles to one fileRef
    target = project.get_target_by_name(targetName)
    buildFile = checkHeader(project, buildfiles, target)
    if buildFile:  # If the buildfile for specific target exist, we modify
        buildFile.settings.ATTRIBUTES = [headerScope]
        return

    fileOptions = FileOptions(header_scope=headerScope)
    file_type, expected_build_phase = ProjectFiles._determine_file_type(fileObj, fileOptions.ignore_unknown_type)
    buildFile = project._create_build_files(fileObj, targetName, expected_build_phase, fileOptions)

    return buildFile

if __name__ == '__main__':
    test = GroupStruct(project)
    a = addExistingFileToHeader(project, project.get_files_by_name('AAPLAppDelegate.h')[0], targetName = 'CloudSearch')
    print(a)
    project.save()