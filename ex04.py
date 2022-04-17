class FileSystem:  # Initiates file system.
    def __init__(self, root):
        self.root = root
        self.current = root  # self.parents = []

    def pwd(self):  # Prints the working directory.
        print("The current working directory is:")
        print("\'", end="")
        print(self.current.filename, end="")
        print("\'")

    def ls(self, arg):  # Creates a list of the working directory.
        self.current.ls(arg)

    def cd(self, directory_name):  # Changes directory.
        if directory_name != "..":
            is_exist = False  # Sets this variable as false until a directory is identified to move to.
            for child in self.current.children:
                if (child.filename == directory_name) and (child.__class__.__name__ == "Directory"):
                    self.current = child

                    is_exist = True  # If the directory the user input exists then change the directory and make a
                    # print out that they did.
                    print("You have changed directory to:")
                    print("\'", end="")
                    print(self.current, end="")
                    print("\'")
                    break

            if not is_exist:  # If directory doesn't exist then tell the user.
                print("The directory does not exist!")

        else:
            if self.current.parent == "":  # If the directory is '..' then return
                return

            self.current = self.current.parent  # Climbs back up the directory tree to root.
            print("You have climbed up the directory tree to the directory:")
            print(self.current.parent)

    def chown(self, new_owner):  # Updates new owner.
        self.current.chown(new_owner)

    def chown_r(self, owner, directory=None):  # Updates the owner for all files.
        if not directory:
            directory = self.root

        directory.chown(owner)
        for child in directory.children:
            child.chown(owner)

            if child.__class__.__name__ == "Directory":
                self.chown_r(owner, child)

    def create_file(self, name):  # Creates new file.
        file = PlainFile(name)
        owner = input("Who owns the file : ")  # Allows the user to input a new owner.
        file.chown(owner)

        is_exist = False  # If the file exists then print that it exists.
        for child in self.current.children:
            if (child.filename == name) and (child.__class__.__name__ == "PlainFile"):
                is_exist = True
                print("File already exists!")
                break

        if not is_exist:  # If it doesn't exist, creates it.
            self.current.children.append(file)

    def mkdir(self, name):  # Makes a new directory and assigns the owner.
        directory = Directory(name, [])
        owner = input("Who owns the directory : ")
        directory.chown(owner)

        is_exist = False  # Breaks if the directory already exists.
        for child in self.current.children:
            if (child.filename == name) and (child.__class__.__name__ == "Directory"):
                is_exist = True
                print("Directory already exists!")
                break

        if not is_exist:  # If it doesn't exist then adds to the list of directories via append.
            self.current.children.append(directory)

    def rm(self, name):  # Removes a file or directory.
        delete_index = -1
        for index in range(len(self.current.children)):
            if self.current.children[index].filename == name:
                if self.current.children[index].__class__.__name__ == "PlainFile":
                    delete_index = index
                    print("You have deleted the index:")
                    print(self.current.children[index])
                    break
                else:  # If there are > 0 entries in the index then does not allow the user to delete and breaks.
                    if len(self.current.children[index].children) != 0:
                        print("Sorry, the directory is not empty")
                        delete_index = -2
                        break

                    else:
                        delete_index = index
                        break

        if delete_index >= 0:
            del self.current.children[delete_index]

        elif delete_index == -1:
            print("Not found")

    def find(self, name):  # Finds the file or directory.
        directories = [self.current]
        file = None

        while (len(directories) != 0) and (not file):
            temp = directories[0]

            for child in temp.children:
                if child.filename == name:
                    file = child
                    break

                if child.__class__.__name__ == "Directory":
                    directories.append(child)
            del directories[0]

        if file:
            path = file.filename

            while file.parent != "":
                path = file.parent.filename + "/" + path
                file = file.parent

            print("\'" + path + "\'")

        else:
            print("Sorry, there was a problem with your input.")  # Error printout.

    def mv(self, current_path, destination_path):  # Moves a file.
        path_dirs = current_path.split("/")  # Splits the current path into a list of strings using / as a delimiter.
        dest_dirs = destination_path.split("/")  # Splits the destination path into a list of strings using / as a
        # delimiter.

        current_dir = self.root

        index = -1
        for i in range(len(path_dirs)):
            for j in range(len(current_dir.children)):
                if current_dir.children[j].filename == path_dirs[i]:

                    if i == len(path_dirs) - 1:
                        index = j

                    current_dir = current_dir.children[j]
                    break

        dest_dir = self.root
        for i in range(len(dest_dirs)):
            for child in dest_dir.children:
                if child.filename == dest_dirs[i]:
                    dest_dir = child
                    break

        dest_dir.children.append(current_dir)
        del current_dir.parent.children[index]

class File:  # Creates the file class.
    def __init__(self, filename):
        self.owner = "default"  # Makes the owner 'default' by default as instructed.
        self.filename = filename  # Initialises a filename.
        self.parent = ""  # Initialises parent.

    def chown(self, new_owner):  # Intiialises chown
        self.owner = new_owner  # Changes default to the new owner when this is called.

    def __str__(self):
        return self.filename  # Returns the current filename.

    def getDetails(self):
        return self.filename + " (" + self.owner + ")"  # Displays file owner of file.


class PlainFile(File):  # Initialises the PlainFile class.
    def __init__(self, filename):
        File.__init__(self, filename)


class Directory(File):  # Initialises the directory.
    def __init__(self, filename, children):
        File.__init__(self, filename)
        self.children = children
        for child in self.children:
            child.parent = self

    def ls(self, tab_spaces=0):  # Lists all files in the directory.

        print('\t' * tab_spaces, end="")
        print(self)
        tab_spaces += 1  # Accumulates the number of tabs necessary for the directory indentation.

        for child in self.children:
            if child.__class__.__name__ == "PlainFile":
                print('\t' * tab_spaces, end="")
                print(child)
            else:
                child.ls(tab_spaces)

    def ls(self, arg, tab_spaces=0):  # Adds owner of file in the printout - still not working.

        print('\t' * tab_spaces, end="")
        if arg == 'l':
            print(self.getDetails())

        else:  # If not, then just indents.
            print(self)
        tab_spaces += 1

        for child in self.children:  # Prints the owner.
            if child.__class__.__name__ == "PlainFile":
                print('\t' * tab_spaces, end="")
                if arg == 'l':
                    print(child.getDetails())

                else:
                    print(child)
            else:
                child.ls(arg, tab_spaces)





# Initialises the file system.
root = Directory("root",
                 [PlainFile("boot.exe"),
                  Directory("home", [
                      Directory("thor",
                                [PlainFile("hunde.jpg"),
                                 PlainFile("quatsch.txt")]),
                      Directory("isaac", [PlainFile("gatos.jpg")])])])

fs = FileSystem(root)  # Passes the initialised root file system into the FileSystem class.


def printUsage():  # Displays a list of commands that the user can use to interact with the file system.
    print("Welcome to the file system!\n"
          "Instructions :")
    print("\tls - shows contents of a directory and all the content of all subdirectories\n"
          "\tls -l - shows contents of a directory with owner\n"
          "\tpwd - shows the current working directory\n"
          "\tcd <directory_name> - changes directory - start by moving to the home directory\n"
          "\tchown -r <owner> - changes owner\n"
          "\ttouch <filename> - creates file\n"
          "\tmkdir <directory_name> - creates directory\n"
          "\trm <name> - removes directory or plain file\n"
          "\tfind <name> - finds file and show the path\n"
          "\tmv <current_path> <destination_path> moves a file")


printUsage()  # Calls printUsage to allow the user to know that the program has begun and also what to do.
while True:
    data = input(">>").lower()  # Asks for input and converts it to lowercase.
    command = data.split()  # Splits the string input into a list where each word is a list item to allow for flags.
    if (len(command) == 1) and (
            command[0] == "ls"):  # Set of if statements to differentiate between a normal ls command
        # and a flag.
        fs.ls('')

    elif (len(command) == 2) and (command[0] == "ls") and (command[1] == "-l"):
        fs.ls('l')

    elif command[0] == "pwd":  # Prints working directory.
        fs.pwd()

    elif command[0] == "cd":  # Changes directory.
        fs.cd(command[1])

# This still is not working properly.
    elif command[0] == "chown" and command[1] == "-r":  # Changes owner of all files/directories.
        option = input(
            "Should these permissions be applied to all files in the system or just one?\n"
            "Enter ‘all’ or ‘one’? ").lower()

        while option not in ["all", "one"]:  # Could not find a way of doing this that wasn't in lectures or the book.
            print("Invalid Input")
            option = input(
                "Should these permissions be applied to all files in the system or just one?\n"
                "Enter ‘all’ or ‘one’? ").lower()  # Converts to lower case.

        if option == "all":  # If the user selects all, then all files belong to owner.
            fs.chown_r(command[2])

        else:  # If not, then just one will.
            fs.chown(command[2])



    elif command[0] == "touch":  # Creates a file.
        fs.create_file(command[1])

    elif command[0] == "mkdir":  # Makes a directory.
        fs.mkdir(command[1])

    elif command[0] == "rm":  # Removes a file or directory.
        fs.rm(command[1])

    elif command[0] == "find":  # Finds a file or directory.
        fs.find(command[1])

    elif command[0] == "mv":  # Moves a file or directory.
        fs.mv(command[1], command[2])

    else:  # Calls printUsage.
        printUsage()

