## Instruction of design

The command interface is responsible for extracting command line.
The Application interface is responsible for detailed operations.
The command interface create a commandStream class.
The Application interface receive the class and passing useful parameters to applications.

## commandStream class design

### parameters
1. currDir -> String
2. stdout -> TextIO
3. stdin -> TextIO
4. path -> str
5. files -> [str]
6. options -> dict
7. pattern str
### functions

1. setCurrDir(self,currDir:String) -> None
2. getCurrDir(self) -> List[Str]

###
1. getFiles(self) -> List[Str]
2. addFiles(self,arg:string) -> None
###
1. addOptions(self,key:str,val) -> None
2. getOptions(self,key:string) -> val
###
1. getStdout(self) -> TextIO
2. setStdout(self,stdout:TextIO) -> None
###
1. getStdin(self) -> TextIO
2. setStdin(self,stdin:TextIO) -> None
###
1. getPath(self) -> str
2. setPath(self,path:str) -> None
###
1. getPattern(self) -> str
2. setPattern(self,pattern:str) -> None