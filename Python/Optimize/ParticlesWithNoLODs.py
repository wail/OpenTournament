import unreal
import sys
import os

notepadFilePath = os.path.dirname(__file__) + "/Output.txt"

if (len(sys.argv) > 1):
    workingPath = sys.argv[1]
else:
    workingPath = "/Game/" # Using the root directory

EditAssetLib = unreal.EditorAssetLibrary()
SystemsLib = unreal.SystemLibrary
StringLib = unreal.StringLibrary()
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0


with unreal.ScopedSlowTask(len(allAssets), selectedAssetsPath) as ST:
    ST.make_dialog(True)

    for asset in allAssets:
        _assetData = EditAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()
        # unreal.log(_assetClassName)

        if _assetClassName == "ParticleSystem":
            _ParticleAssetNumLODS = len(_assetData.get_asset().get_editor_property("lod_settings"))

            if _ParticleAssetNumLODS <= 1:
                LogStringsArray.append("        %s ------------> At Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("Asset Name: %s [No Asset Plugged In] Path: %s \n" % (_assetName, _assetPathName))
                numOfOptimisations += 1

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Particles With No LODs"
DescOfOptimisation = "Searches the entire project for particles that have no LODs setup"
SummaryMessageIntro = "-- Particles With No LODs --"

if unreal.Paths.file_exists(notepadFilePath):  # Check if txt file already exists
    os.remove(notepadFilePath)  # if does remove it

# Create new txt file and run intro text
file = open(notepadFilePath, "a+")  # we should only do this if have a count?
file.write("==================================================================================================== \n")
file.write("    SCRIPT NAME: %s \n" % TitleOfOptimisation)
file.write("    DESCRIPTION: %s \n" % DescOfOptimisation)
file.write("==================================================================================================== \n \n")


if numOfOptimisations <= 0:
    file.write(" -- NONE FOUND -- \n \n")
else:
    for i in range(len(LogStringsArray)):
        file.write(LogStringsArray[i])


# Run summary text
file.write("\n")
file.write("======================================================================================================= \n")
file.write("    SUMMARY: \n")
file.write("        %s \n" % SummaryMessageIntro)
file.write("              Found: %s \n \n" % numOfOptimisations)
file.write("======================================================================================================= \n")
file.write("        Logged to %s \n" % notepadFilePath)
file.write("======================================================================================================= \n")
file.close()
os.startfile(notepadFilePath)  # Trigger the notepad file to open
