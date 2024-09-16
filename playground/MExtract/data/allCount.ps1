# Loop through all .txt files in the current directory
Get-ChildItem -Filter *.txt | ForEach-Object {
    $fileName = $_.Name
    $count = & nonEmptyCount.ps1 -FilePath $fileName | Out-String | Select-String -Pattern "Number of non-empty lines" | ForEach-Object {
        $_ -replace '.*Number of non-empty lines in .+: ', ''
    }
    
    Write-Output "$fileName => $count"
}
