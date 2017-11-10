C:
set dbpath="C:\Program Files\MongoDB\Server\3.4\data\db"
if exist dbpath (goto run) else md %dbpath%

:run
CD C:\Program Files\MongoDB\Server\3.4\bin
mongod --dbpath="C:\Program Files\MongoDB\Server\3.4\data\db"

pause