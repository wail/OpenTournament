import unreal
import sys
import os

notepadFilePath = os.path.dirname(__file__) + "/Output.txt"

if (len(sys.argv) > 1):
    workingPath = sys.argv[1]
else:
    workingPath = "/Game/" # Using the root directory

EditAssetLib = unreal.EditorAssetLibrary()
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

        if _assetClassName == "Material":
            _MaterialAsset = unreal.Material.cast(_assetData.get_asset())
            # unreal.log(_MaterialAsset.blend_mode)

            if _MaterialAsset.blend_mode == unreal.BlendMode.BLEND_TRANSLUCENT:
                LogStringsArray.append("        %s ------------> At Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("is a translucent material")
                numOfOptimisations += 1

        """
        # material instances have no blend mode stuff exposed atm so cant do this
        elif _assetClassName == "MaterialInstanceConstant":
            asset_obj = EditAssetLib.load_asset(asset)
            _MaterialInstanceAsset = unreal.MaterialInstance.cast(_assetData.get_asset())
            # unreal.log(_MaterialAsset.blend_mode)

            if _MaterialInstanceAsset.blend_mode == unreal.BlendMode.BLEND_TRANSLUCENT:
                LogStringsArray.append("        [MIC] %s ------------> At Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("is a translucent material instance")
                numOfOptimisations += 1
        """

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Materials Using Translucency"
DescOfOptimisation = "Searches the entire project for materials that are using Translucency (master materials only, does not check material instances)"
SummaryMessageIntro = "-- Materials Using Translucency --"

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
