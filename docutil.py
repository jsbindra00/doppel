# ███╗░░██╗░░███╗░░░██████╗░██╗░░██╗████████╗██████╗░██╗██████╗░██████╗░██████╗░
# ████╗░██║░████║░░██╔════╝░██║░░██║╚══██╔══╝██╔══██╗██║██╔══██╗╚════██╗██╔══██╗
# ██╔██╗██║██╔██║░░██║░░██╗░███████║░░░██║░░░██████╔╝██║██║░░██║░█████╔╝██████╔╝
# ██║╚████║╚═╝██║░░██║░░╚██╗██╔══██║░░░██║░░░██╔══██╗██║██║░░██║░╚═══██╗██╔══██╗
# ██║░╚███║███████╗╚██████╔╝██║░░██║░░░██║░░░██║░░██║██║██████╔╝██████╔╝██║░░██║
# ╚═╝░░╚══╝╚══════╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═════╝░╚═════╝░╚═╝░░╚═╝
################## be good and code until you die - socrates. ##################
import os
import shutil

class DocUtil:
    def RenameFile(src, dest):
        os.rename(src, dest)
    def RemoveExtension(dir):
        return os.path.splitext(dir)[0]
    def MoveFile(old_dir, new_dir):
        os.replace(old_dir,new_dir)
    def ListAllFolders(directory):
        return [f.path for f in os.scandir(directory) if f.is_dir()]
    def ListAllFiles(directory):
        return [f.path for f in os.scandir(directory) if f.is_file()]
    def GetExtension(path):
        return os.path.splitext(path)[1]
    def ConvertStringToDir(dirString):
        return dirString.replace('\\', '\\\\')
    def RemoveFile(filename):
        if os.path.exists(filename):
            os.remove(filename)
    def ItemExists(directory, fileName):
        os.chdir(directory)
        return DocUtil.RootPlusLeaf(directory, fileName) if os.path.exists(fileName) else None
    def ItemExists(path):
        return path if os.path.exists(path) else None
    def PathLeaf(directory):
        return os.path.basename(directory)
    def MakeFile(path, filename):
        os.chdir(path)
        open(filename, 'a').close()
    def AddExtension(fileName, extension):
        return "{}.{}".format(fileName, extension)
    def ReadFile(filePath):
        try:
            file = open(filePath, "r")
            return file.read()
        except:
            file = open(filePath, "a")
            return DocUtil.ReadFile(filePath)

    def RootPlusLeaf(root, leaf):
        return os.path.join(root, leaf)
    def CreateFolder(root, folderName):
        dir = DocUtil.RootPlusLeaf(root,folderName)
        os.mkdir(dir)
        return dir
    def CreateFolderAbsoluteDirectory(root):
        os.mkdir(root)
        return root
    def CopyFile(source, dest):
        return shutil.copy2(source, dest)
    def CopyFiles(dest, sourceFiles):
        for file in sourceFiles:
            DocUtil.CopyFile(dest,file)
    def DeleteFolder(path):
        shutil.rmtree(path)

    def CreateFile(rootDir, fileName, initStr = None):
        f = open(DocUtil.RootPlusLeaf(rootDir, fileName), "w")
        if f is None:
            print("fuck")
        if initStr is not None:
            f.write(initStr)
        f.close()        
    def DirWithoutLeaf(dir):
        return os.path.dirname(dir)
    def GetLeafWithoutExtension(dir):
        return DocUtil.RemoveExtension(DocUtil.PathLeaf(dir))
    
    def ReplaceLeaf(dir, new_leaf):
        return DocUtil.RootPlusLeaf(DocUtil.DirWithoutLeaf(dir), new_leaf)


    # def CopyFilesFrom(src, file_selector, dest):
    #     all_folders = DocUtil.ListAllFolders(src)
    #     all_files = []
    #     for folder, j in zip(all_folders, range(len(all_folders))):
    #         folder_files = DocUtil.ListAllFiles(folder)
    #         for file in folder_files:
    #             extension = DocUtil.GetExtension(file)
    #             if extension == ".png":
    #                 try:
    #                     new_name = "render_" + str(j) + ".png"
    #                     DocUtil.CopyFile(file, DocUtil.RootPlusLeaf(dest, new_name))
    #                     DocUtil.CopyFile(file, dest)
    #                 except Exception as e:
    #                     print(e)



    def CopyFilesToFolders():
        from_ = r"D:\FILES\Desktop\Strucha\Stocklist\stage\final_render_eyebrows.psd"
        src = r"D:\FILES\Desktop\Strucha\Stocklist\stage"
        all_folders = DocUtil.ListAllFolders(src)
        
        for folder in all_folders:
            folder_name = DocUtil.PathLeaf(folder)
            if folder_name == "1" or folder_name == "2":
                continue
            # for file in DocUtil.ListAllFiles(folder):
            #     if DocUtil.PathLeaf(file) == "final_render_eyebrows_no_bg.psd":
            #         DocUtil.RemoveFile(file)
            DocUtil.CopyFile(from_, folder)

    def CopyFileTypeToDestination(src, dest):
        all_folders = DocUtil.ListAllFolders(src)

        for folder, i in zip(all_folders, range(len(all_folders))):
            for file in DocUtil.ListAllFiles(folder):
                if DocUtil.PathLeaf(file) == "final_render_eyebrows.png":
                    new_file_name = DocUtil.RemoveExtension(DocUtil.PathLeaf(file)) + "_" + str(i) + ".png"
                
                    DocUtil.CopyFile(file, DocUtil.RootPlusLeaf(dest, new_file_name))


    

    def CopyFilesFrom(src, file_selector, dest):
        all_folders = DocUtil.ListAllFolders(src)
        all_files = []
        for folder, j in zip(all_folders, range(len(all_folders))):
            folder_files = DocUtil.ListAllFiles(folder)
            for file in folder_files:
                extension = DocUtil.GetExtension(file)
                leaf = DocUtil.PathLeaf(file)
                leaf_no_extension = DocUtil.RemoveExtension(leaf)

                if extension == ".png":
                    if leaf_no_extension.lower() == "final_render":

                        DocUtil.CopyFile(file, DocUtil.RootPlusLeaf(dest, leaf_no_extension + "_"+ str(j + 1) + ".png"))
                        # new_file_name = DocUtil.RootPlusLeaf(DocUtil.DirWithoutLeaf(file), "original_process.psd")

                        # print(leaf_no_extension)
                        # print(j)
                        # DocUtil.CopyFile(new_file_name, render_name)

                    try:
                        new_file_name = DocUtil.RootPlusLeaf(DocUtil.DirWithoutLeaf(file), "original_process.psd")
                        render_name = DocUtil.RootPlusLeaf(DocUtil.DirWithoutLeaf(file), "final_render.psd")

                        # DocUtil.CopyFile(new_file_name, render_name)
                        # DocUtil.RenameFile(file, new_file_name)
                        
                        # DocUtil.CopyFile(file, DocUtil.RootPlusLeaf(target_dir, "original_process.psd"))
                    except Exception as e:
                        print(e)





src = r"D:\FILES\Desktop\Strucha\Stocklist\stage"
dest = r"D:\FILES\Desktop\Strucha\Stocklist\stage\export stage\final_renders"










