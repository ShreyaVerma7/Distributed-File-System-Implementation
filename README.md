# Distributed-File-System-Implementation
![DFS](https://github.com/ShreyaVerma7/Distributed-File-System-Implementation/blob/main/Schematic%20diagram%20of%20DFS.png)

## Components
*	Distributed System Node: These represent the “clients” in DFS architecture. They allow users to interact with files stored on File Servers and execute various commands.
*	File Server: These store files in the file system. They allow Distributed System Nodes to interact with the files using Remote Procedure Calls only with proper authentication.
*	Key Distribution Centre: The KDC shares symmetric keys with the nodes in the system. The file servers register with the KDC for the files that are stored. The KDC grants the distributed system nodes session keys for mutual authentication.

## Working of System
*	All the file servers FSi and the distributed nodes DSi must be assigned unique ids and share symmetric keys with a Key Distribution Server (KDC). 
*	All the File servers register with the KDC for the files that they store. 
*	The Distributed nodes authenticate with the KDC to generate session key using the symmetric key mutual authentication protocol. 
*	The DS must mutually authenticate the file server and get the files they display in a folder for the file server. **Needham-Schroeder** protocol will be used for mutual authentication. 
*	FSi must register any new file that is created with KDC. 
*	File creation must be communicated to all DSi as a folder entry seen on the shell.

##	Functionalities
*	Implementation of RPCs to establish a secure connection between distributed nodes and file servers in the DFS.
* File Server registration and set-up.
*	Distributed Node registration and authentication with servers.
*	Commands that are listed below:
    *	**pwd** – list the present working directory
    * **ls** – list contents of the file
    * **cp** – copy one file to another in the same folder
    * **cat** – display contents of the file
