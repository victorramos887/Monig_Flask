$databaseHost = 'ec2-44-213-228-107.compute-1.amazonaws.com'
$databasePort = 5432
$databaseName = 'd2rhs4sdgd6ka7'
$databaseUser = 'mpelsrzlxcmjzp'
$databasePassword = '8a0130b05b865dd180d5bba8d6b54fbaba2e2886da2b6de127f4ee89bbab35fa'

$env:PGPASSWORD = $databasePassword
$command = "psql.exe -h $databaseHost -p $databasePort -U $databaseUser -d $databaseName"

Start-Process -FilePath $command
